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