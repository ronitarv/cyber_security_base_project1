from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    is_public = models.BooleanField()