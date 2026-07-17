from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate
from app.models.product import Product, ProductSpecification, ProductInclude
from sqlalchemy.orm import Session

class ProductService:
    @staticmethod
    def create_product(db: Session, product_in: ProductCreate) -> Product:
        # Build the main object
        db_product = Product(
            category_id=product_in.category_id,
            name=product_in.name,
            slug=product_in.slug,
            sku=product_in.sku,
            badge=product_in.badge,
            short_description=product_in.short_description,
            long_description=product_in.long_description,
            price=product_in.price,
            stock_quantity=product_in.stock_quantity,
            is_ready_stock=product_in.is_ready_stock,
            range_km=product_in.range_km,
            flight_time_min=product_in.flight_time_min,
            tags=product_in.tags,
            main_image_url=product_in.main_image_url
        )
        
        # Build nested lists
        for spec in product_in.specifications:
            db_product.specifications.append(ProductSpecification(**spec.model_dump()))
            
        for item in product_in.includes:
            db_product.includes.append(ProductInclude(item_name=item.item_name))
            
        # Hand it to the Repository to save!
        return ProductRepository.create(db, db_product)

    @staticmethod
    def get_all_products(db: Session, skip: int = 0, limit: int = 100):
        return ProductRepository.get_all(db, skip=skip, limit=limit)