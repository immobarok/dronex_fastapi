from sqlalchemy.orm import Session
from app.models.product import Product
class ProductRepository:
    @staticmethod
    def create(db:Session,db_product:Product)-> Product:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product