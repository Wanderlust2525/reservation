from django.contrib.auth import get_user_model
from account.models import User as UserModel

User: UserModel = get_user_model()