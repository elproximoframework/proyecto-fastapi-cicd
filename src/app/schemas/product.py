from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., examples=["Widget A"])
    description: Optional[str] = Field(None, examples=["A useful widget"])
    price: float = Field(..., gt=0, examples=[19.99])
    stock: int = Field(0, ge=0, examples=[100])


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
