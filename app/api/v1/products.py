from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.api.deps import get_current_admin_user
from app.models.user import User
from app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate
from app.schemas.response import StandardResponse
from fastapi.routing import APIRouter
from typing import List
from app.schemas.product import ProductCreate, ProductResponse
router=APIRouter()

@router.post(
    "/create", 
    response_model=StandardResponse, 
    dependencies=[Depends(get_current_admin_user)] 
)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = ProductService.create_product(db, product_in)
    
    return StandardResponse(
        success=True,
        message="Product created successfully",
        data={"id": new_product.id, "name": new_product.name}
    )

@router.get("/", response_model=StandardResponse[List[ProductResponse]])
def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_products = ProductService.get_all_products(db, skip=skip, limit=limit)
    return StandardResponse(
        success=True,
        message="All products fetched successfully",
        data=all_products
    )