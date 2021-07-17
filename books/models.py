from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    pass
# Create your models here.
class books(models.Model):
    bookID=models.IntegerField(null=False)
    title=models.CharField(max_length=500)
    author=models.CharField(max_length=500)
    average_ratting=models.CharField(max_length=100)
    publisher=models.CharField(max_length=500)
    summary=models.TextField(null=True)

class Click(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    last_click=models.ForeignKey(books,on_delete=models.CASCADE)