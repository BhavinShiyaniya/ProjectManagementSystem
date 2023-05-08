from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# class Role(models.Model):
#     roleName = models.CharField(max_length=20,null=False,unique=True)

#     createdtime = models.DateTimeField(auto_now_add=True)
#     updatedtime = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.roleName

#     class Meta:
#         db_table = 'Role'

class User(AbstractUser):
    # role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_teamleader = models.BooleanField(default=False)
    is_tester = models.BooleanField(default=False)

    createdtime = models.DateTimeField(auto_now_add=True)
    updatedtime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'user'

# class User(models.Model):
#     firstName = models.CharField(max_length=30)
#     email = models.EmailField(max_length=30)
#     password = models.CharField(max_length=30)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)

#     createdtime = models.DateTimeField(auto_now_add=True)
#     updatedtime = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.firstName

#     class Meta:
#         db_table = 'User'



