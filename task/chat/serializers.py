
from rest_framework import serializers
from .models import Message,User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        read_only_fields = ('id', 'username', 'email')

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model=Message
        fields = ('id','sender','receiver', 'subject', 'message','creationdate','read')
        read_only_fields = ('id','sender','creationdate','read')
