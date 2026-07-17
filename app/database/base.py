# Import all the models, so that Base has them before being
# imported by Alembic
from app.database.base_class import Base
from app.models.user import User

# Import other models here when you create them
