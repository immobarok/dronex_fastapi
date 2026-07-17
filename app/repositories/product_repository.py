from sqlalchemy.orm import Session
from app.models.product import Product
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
                
            # 2. Update only the fields that were provided
            for key, value in update_data.items():
                setattr(product, key, value)
                
            # 3. Save to database
            db.commit()
            db.refresh(product)
            return product
        except Exception as e:
            db.rollback()
            return None