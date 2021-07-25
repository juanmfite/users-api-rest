from django.contrib.auth.models import AbstractUser, User as UserBaseModel
from django.db import models


class User(AbstractUser):

    updated = models.DateTimeField(
        auto_now=True,
    )

    @property
    def staff_or_superuser(self):
        return self.is_staff or self.is_superuser
