from typing import Union

from app.core.schemas.category import CategoryDeletion
from app.db.models.category import Category
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore
from starlette.status import HTTP_200_OK


async def get_all_categories(db: Session):
    return db.query(Category).all()


async def get_category_by_id(db: Session, category_id: int) -> Union[Category, None]:
    return db.query(Category).filter(Category.category_id == category_id).first()


async def get_category_by_name(db: Session, category_name: str) -> Union[Category, None]:
    return db.query(Category).filter(Category.category_name == category_name).first()


async def create_category(db: Session, category_name: str):
    if await get_category_by_name(db, category_name) is not None:
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail=f"The category {category_name} is already created",
        )
    category = Category(category_name=category_name)
    db.add(category)
    db.commit()
    db.refresh(category)
    category = db.query(Category).filter(Category.category_name == category_name).first()
    assert category is not None, f"could not create category {category_name}"
    return category


async def delete_category(db: Session, category_name: str):

    category = await get_category_by_name(db, category_name)
    if category:
        db.delete(category)
        db.commit()
    else:
        raise HTTPException(status_code=HTTP_200_OK, detail=f"The category with the name {category_name} is not found")
    return CategoryDeletion(category_name=category_name, delete_status=True)
