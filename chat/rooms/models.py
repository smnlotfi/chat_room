from venv import create
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

user=get_user_model()


class room(models.Model):
    name=models.CharField(max_length=50)
    create_time=models.TimeField(auto_now=True)
    members=models.ManyToManyField(user,blank=True,null=True)


    def __str__(self):
        return self.name

    def get_all_room(self):
        return self.objects.all()
