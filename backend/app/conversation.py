from sqlalchemy.ext.asyncio import AsyncSession
from .crud import get_conversation, upsert_conversation, delete_conversation, create_review

STEP_ASK_PRODUCT = "ask_product"
STEP_ASK_NAME = "ask_name"
STEP_ASK_REVIEW = "ask_review"

async def handle_inbound_message(db: AsyncSession, contact: str, text: str):
    """
    Returns tuple (reply_text, finished_flag)
    reply_text: string to send back to user
    finished_flag: True if conversation finished and review saved
    """
    # normalize text
    content = text.strip()

    # fetch conversation
    state = await get_conversation(db, contact)

    # If no state or user sends hi/start, start the flow
    if not state or content.lower() in ("hi", "hello", "start"):
        await upsert_conversation(db, contact, STEP_ASK_PRODUCT)
        return "Which product is this review for?", False

    # if asking for product
    if state.step == STEP_ASK_PRODUCT and not state.product_name:
        product = content
        await upsert_conversation(db, contact, STEP_ASK_NAME, product=product)
        return "What's your name?", False

    # if asking for name
    if state.step == STEP_ASK_NAME and not state.user_name:
        user = content
        # preserve product in DB (state.product_name)
        await upsert_conversation(db, contact, STEP_ASK_REVIEW, user=user)
        product_display = state.product_name if state.product_name else "the product"
        return f"Please send your review for {product_display}.", False

    # if asking for review
    if state.step == STEP_ASK_REVIEW:
        product = state.product_name or "the product"
        user = state.user_name or "Customer"
        review_text = content
        # save review
        await create_review(db, contact, user, product, review_text)
        # clear conversation state
        await delete_conversation(db, contact)
        return f"Thanks {user} -- your review for {product} has been recorded.", True

    # fallback: reset
    await upsert_conversation(db, contact, STEP_ASK_PRODUCT)
    return "Which product is this review for?", False
