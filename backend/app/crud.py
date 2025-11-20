from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Review, ConversationState
from datetime import datetime

async def get_all_reviews(db: AsyncSession):
    result = await db.execute(select(Review).order_by(Review.created_at.desc()))
    return result.scalars().all()

async def get_conversation(db: AsyncSession, contact: str):
    result = await db.execute(select(ConversationState).where(ConversationState.contact_number==contact))
    return result.scalars().first()

async def upsert_conversation(db: AsyncSession, contact: str, step: str, product: str | None = None, user: str | None = None):
    existing = await get_conversation(db, contact)
    if existing:
        existing.step = step
        if product is not None:
            existing.product_name = product
        if user is not None:
            existing.user_name = user
    else:
        existing = ConversationState(contact_number=contact, step=step, product_name=product, user_name=user)
        db.add(existing)
    await db.commit()
    await db.refresh(existing)
    return existing

async def delete_conversation(db: AsyncSession, contact: str):
    await db.execute(delete(ConversationState).where(ConversationState.contact_number==contact))
    await db.commit()

async def create_review(db: AsyncSession, contact: str, user_name: str, product_name: str, product_review: str):
    rev = Review(contact_number=contact, user_name=user_name, product_name=product_name, product_review=product_review)
    db.add(rev)
    await db.commit()
    await db.refresh(rev)
    return rev
