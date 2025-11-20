from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_db
from .crud import get_all_reviews

router = APIRouter()

@router.get("/api/reviews")
async def api_get_reviews(db: AsyncSession = Depends(get_db)):
    reviews = await get_all_reviews(db)
    # return JSON-serializable list
    out = []
    for r in reviews:
        out.append({
            "id": r.id,
            "contact_number": r.contact_number,
            "user_name": r.user_name,
            "product_name": r.product_name,
            "product_review": r.product_review,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })
    return out
