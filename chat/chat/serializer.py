from pyexpat import model
from attr import field
from rest_framework import serializers
from rooms.models import message
from attr import fields



class message_serializer(serializers.ModelSerializer):


    class Meta:
        model=message
        fields=['__str__','message_send_time','content']