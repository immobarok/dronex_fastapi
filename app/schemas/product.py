from unicodedata import name
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from decimal import Decimal

class ProductSpecificationCreate(BaseModel):
    name:str
    value:str

class ProductIncludeCreate(BaseModel):
    item_name: str

class ProductCreate(BaseModel):
    category_id: int
    name: str
    slug: str
    sku: Optional[str] = None
    badge: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    price: Decimal
    stock_quantity: int = 0
    is_ready_stock: bool = True
    range_km: Optional[Decimal] = None
    flight_time_min: Optional[Decimal] = None
    tags: Optional[List[str]] = None
    main_image_url: Optional[str] = None
    specifications: List[ProductSpecificationCreate] = []
    includes: List[ProductIncludeCreate] = []

class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    sku: Optional[str] = None
    badge: Optional[str] = None
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    is_ready_stock: Optional[bool] = None
    range_km: Optional[Decimal] = None
    flight_time_min: Optional[Decimal] = None
    tags: Optional[List[str]] = None
    main_image_url: Optional[str] = None
    specifications: Optional[List[ProductSpecificationCreate]] = None
    includes: Optional[List[ProductIncludeCreate]] = None

class ProductResponse(ProductCreate):
    id: int
    model_config = {"from_attributes": True}