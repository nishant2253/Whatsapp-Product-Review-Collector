from fastapi import FastAPI
from .db import create_db_and_tables
from .webhook import router as webhook_router
from .reviews import router as reviews_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="WhatsApp Review Collector")

# Allow frontend dev server to call backend (adjust origins in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router)
app.include_router(reviews_router)

@app.on_event("startup")
async def on_startup():
    # create tables if not exist
    await create_db_and_tables()
