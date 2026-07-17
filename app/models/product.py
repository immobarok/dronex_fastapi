from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text, ForeignKey, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime
from app.database.base_class import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    products = relationship("Product", back_populates="category")


# Association table for product compatibility (Many-to-Many self-referential)
product_compatibilities = Table(
    "product_compatibilities",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("compatible_product_id", Integer, ForeignKey("products.id"), primary_key=True),
)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    sku = Column(String, unique=True, index=True)
    badge = Column(String, nullable=True)
    short_description = Column(Text, nullable=True)
    long_description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, default=0)
    is_ready_stock = Column(Boolean, default=True)
    
    # Dynamic Specs
    range_km = Column(Numeric(10, 2), nullable=True)
    flight_time_min = Column(Numeric(10, 2), nullable=True)
    tags = Column(JSONB, nullable=True) # e.g. ["4K", "GPS", "CREATOR"]
    
    # Ratings
    rating_score = Column(Numeric(3, 2), nullable=True)
    review_count = Column(Integer, default=0)
    
    main_image_url = Column(String, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())

    # Relationships
    category = relationship("Category", back_populates="products")
    specifications = relationship("ProductSpecification", back_populates="product", cascade="all, delete-orphan")
    includes = relationship("ProductInclude", back_populates="product", cascade="all, delete-orphan")
    support_features = relationship("ProductSupportFeature", back_populates="product", cascade="all, delete-orphan")
    rating_breakdowns = relationship("ProductRatingBreakdown", back_populates="product", cascade="all, delete-orphan")
    
    # Self-referential Many-to-Many
    compatible_products = relationship(
        "Product",
        secondary=product_compatibilities,
        primaryjoin=id==product_compatibilities.c.product_id,
        secondaryjoin=id==product_compatibilities.c.compatible_product_id,
        backref="compatible_with"
    )

class ProductSpecification(Base):
    __tablename__ = "product_specifications"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)

    product = relationship("Product", back_populates="specifications")

class ProductInclude(Base):
    __tablename__ = "product_includes"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    item_name = Column(String, nullable=False)

    product = relationship("Product", back_populates="includes")

class ProductSupportFeature(Base):
    __tablename__ = "product_support_features"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    feature_name = Column(String, nullable=False)

    product = relationship("Product", back_populates="support_features")

class ProductRatingBreakdown(Base):
    __tablename__ = "product_rating_breakdowns"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    metric_name = Column(String, nullable=False)
    score_percentage = Column(Integer, nullable=False)

    product = relationship("Product", back_populates="rating_breakdowns")
