from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.app.api.dependencies import get_current_user
from src.app.core.database import get_db
from src.app.models.product import Product
from src.app.models.user import User
from src.app.schemas.product import ProductCreate, ProductResponse

router = APIRouter()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    *,
    db: AsyncSession = Depends(get_db),
    product_in: ProductCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """Crea un nuevo producto asociado al usuario autenticado."""
    db_obj = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        stock=product_in.stock,
        owner_id=current_user.id,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@router.get("/", response_model=List[ProductResponse])
async def read_products(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """Obtiene el listado de productos de forma pública."""
    result = await db.execute(select(Product).offset(skip).limit(limit))
    products = result.scalars().all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)) -> Any:
    """Obtiene un producto específico por su ID."""
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.get("/{product_id}/discount", response_model=dict)
async def get_product_discount(
    product_id: int, percentage: float, db: AsyncSession = Depends(get_db)
) -> Any:
    """Calcula el precio final de un producto aplicando un porcentaje de descuento (0-100)."""
    if percentage < 0 or percentage > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discount percentage must be between 0 and 100",
        )

    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    discount_amount = product.price * (percentage / 100)
    final_price = product.price - discount_amount

    return {
        "product_id": product.id,
        "original_price": product.price,
        "discount_percentage": percentage,
        "discount_amount": round(discount_amount, 2),
        "final_price": round(final_price, 2),
    }
