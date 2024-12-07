# import all the models from each module to import in alembic for migrations

from app.user import models as user_models
from app.transaction import models as transaction_models
from app.account import models as account_models
