from django.db.models.signals import pre_save
from django.dispatch import receiver

from account.services import User
from account.models import User as UserModel


@receiver(pre_save, sender=User)
def pre_save_user(sender, instance: UserModel, *args, **kwargs):

    if instance.role == User.ADMIN or instance.is_superuser:
        instance.role = User.ADMIN
        instance.is_superuser = True

    return instance