# Import all the models, so that Base has them before being
# imported by Alembic
from app.database.base_class import Base
from app.models.user import User
from app.models.product import Category, Product, ProductSpecification, ProductInclude, ProductSupportFeature, ProductRatingBreakdown
from app.models.order import Coupon, Cart, CartItem, Order, OrderItem
