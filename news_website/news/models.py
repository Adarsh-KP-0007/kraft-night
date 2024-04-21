from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name=None
    last_name=None
    email=models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    name=models.CharField(max_length=50)
    general=models.BooleanField(default=False)
    business=models.BooleanField(default=False)
    entertainment=models.BooleanField(default=False)
    health=models.BooleanField(default=False)
    science=models.BooleanField(default=False)
    sports=models.BooleanField(default=False)
    technology=models.BooleanField(default=False)
    # politics=models.BooleanField(default=False)
    # world=models.BooleanField(default=False)
    # lifestyle=models.BooleanField(default=False)

    def __str__(self):
        return self.email


