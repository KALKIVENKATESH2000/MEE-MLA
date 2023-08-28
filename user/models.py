from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


def upload(instance, filename):
    return 'uploads/folder/{filename}'.format(filename=filename)

# class CustomUser(AbstractUser):
#     email           = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=250)
    
#     USERNAME_FIELD  = 'email'
#     REQUIRED_FIELDS = ['member_id', 'username']

#     def __str__(self):
#         return self.first_name + " " + self.last_name