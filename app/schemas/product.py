from unicodedata import name
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from decimal import Decimal

class ProductSpecificationCreate(BaseModel):
    name:str
    value:str

class ProductIncludeCreate(BaseModel):
    name:str

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