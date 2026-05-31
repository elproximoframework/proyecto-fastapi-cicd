from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.app.api.dependencies import get_current_user
from src.app.core.database import get_db
from src.app.core.security import get_password_hash
from src.app.models.user import User
from src.app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    *, db: AsyncSession = Depends(get_db), user_in: UserCreate
) -> Any:
    """Registra un nuevo usuario en la base de datos."""
    # Verificar si el email ya está registrado
    result = await db.execute(select(User).filter(User.email == user_in.email))
    user = result.scalars().first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already registered in the system.",
        )

    # Crear nuevo objeto User con contraseña hasheada
    db_obj = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_superuser=user_in.is_superuser,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: User = Depends(get_current_user)) -> Any:
    """Obtiene los datos del perfil del usuario actualmente autenticado."""
    return current_user


@router.get("/", response_model=List[UserResponse])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),  # Requiere autenticación
) -> Any:
    """Obtiene una lista de todos los usuarios registrados."""
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users
