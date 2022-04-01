from pyexpat import model
from attr import field
from rest_framework import serializers
from rooms.models import message
from attr import fields
from django.contrib.auth import get_user_model


user=get_user_model()


class message_serializer(serializers.ModelSerializer):


    class Meta:
        model=message
        fields=['__str__','message_send_time','content']


class user_serializer(serializers.ModelSerializer):


    class Meta:
        model=user
        fields=['username']