from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate
from app.models import Product
from sqlalchemy.orm import Session
class ProductService:
    @staticmethod
    def create_product(db:Session, product_in:ProductCreate)->Product:
        db_product = Product(
            category_id=product_in.category_id,
            name=product_in.name,
            description=product_in.description,
            price=product_in.price,
            image_url=product_in.image_url,
            weight_kg=product_in.weight_kg,
            is_active=product_in.is_active
        )

        for spec in product_in.specifications:
            db_product.specifications.append(**spec.model_dump())
        for item in product_in.items_included:
            db_product.items_included.append(item_name=item.name)
            return ProductRepository.create(db, db_product)
        
        