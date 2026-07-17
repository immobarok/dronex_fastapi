from sqlalchemy.orm import Session
from app.models.product import Product, ProductSpecification, ProductInclude

class ProductRepository:
    @staticmethod
    def create(db:Session,db_product:Product)-> Product:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(Product).filter(Product.id == id).first()

    @staticmethod
    def get_by_slug(db: Session, slug: str):
        return db.query(Product).filter(Product.slug == slug).first()

    @staticmethod
    def delete_single_product(db:Session,id:int):
        try:
            db.query(Product).filter(Product.id == id).delete()
            db.commit()
            return True
        except:
            return False

    @staticmethod
    def update_single_product(db:Session, id:int, update_data: dict):
        try:
            # 1. Fetch the existing product
            product = db.query(Product).filter(Product.id == id).first()
            if not product:
                return None
                
            # Handle Nested Relationships explicitly (delete old, insert new)
            if "specifications" in update_data:
                db.query(ProductSpecification).filter(ProductSpecification.product_id == id).delete()
                for spec in update_data["specifications"]:
                    product.specifications.append(ProductSpecification(**spec))
                del update_data["specifications"]
                
            if "includes" in update_data:
                db.query(ProductInclude).filter(ProductInclude.product_id == id).delete()
                for item in update_data["includes"]:
                    product.includes.append(ProductInclude(**item))
                del update_data["includes"]
                
            # 2. Update the remaining simple fields
            for key, value in update_data.items():
                setattr(product, key, value)
                
            # 3. Save to database
            db.commit()
            db.refresh(product)
            return product
        except Exception as e:
            db.rollback()
            return None