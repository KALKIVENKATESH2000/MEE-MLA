from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


# Create your models here.


def upload(instance, filename):
    return 'uploads/users/{filename}'.format(filename=filename)

# class CustomUser(AbstractUser):
#     email           = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=250)
    
#     USERNAME_FIELD  = 'email'
#     REQUIRED_FIELDS = ['member_id', 'username']

#     def __str__(self):
#         return self.first_name + " " + self.last_name

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

class Profile(models.Model):
    user        = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    full_name   = models.CharField(max_length=50, blank=True, null=True)
    email       = models.CharField(max_length=50, blank=True, null=True)
    phone       = models.CharField(max_length=15,  blank=True, null=True)
    gender      = models.CharField(max_length=10,choices=GENDER_CHOICES,blank=True, null=True)
    image       = models.FileField(upload_to=upload,null=True,blank=True)
    createdAt   = models.DateTimeField(auto_now_add=True)
    updatedAt   = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username