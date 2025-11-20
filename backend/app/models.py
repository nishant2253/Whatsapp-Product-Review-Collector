from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from .db import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    contact_number = Column(Text, nullable=False)
    user_name = Column(Text, nullable=False)
    product_name = Column(Text, nullable=False)
    product_review = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class ConversationState(Base):
    __tablename__ = "conversation_state"
    contact_number = Column(Text, primary_key=True, index=True)
    step = Column(Text, nullable=False)  # ask_product | ask_name | ask_review
    product_name = Column(Text, nullable=True)
    user_name = Column(Text, nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
