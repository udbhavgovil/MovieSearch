from django.db import models

# Create your models here.
class Accounts(models.Model):
    user_id = models.CharField(primary_key=True,max_length=20)
    password = models.CharField(max_length=20)
    Name = models.CharField(max_length=20)
    
class WatchedMovie (models.Model):
    user_id = models.CharField(max_length=20)
    movie_id = models.IntegerField()
    path = models.CharField(max_length=25)

