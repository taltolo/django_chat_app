from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from .serializers import MessageSerializer
from .models import Message,User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import mixins

class userViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
   
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(methods=['post', ], detail=True)
    def read_message(self,request, pk):
        try:
            messageDisplay = Message.objects.get(id=pk)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            messageDisplay.read=True
            messageDisplay.save()
        serializer = MessageSerializer(messageDisplay)
        return Response(serializer.data)

    @action(methods=['GET', ], detail=False)
    def get_messages_by_user(self,request):
        try:
            messagesDisplay=Message.objects.filter(receiver=request.user)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(messagesDisplay, many=True)
        return Response(serializer.data)

    @action(methods=['GET', ], detail=False)
    def get_unread_messages(self,request):
        try:
            messagesDisplay =self.queryset.filter(receiver=request.user).filter(read=False)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(messagesDisplay, many=True)
        return Response(serializer.data)
    
class login(ObtainAuthToken):
    permission_classes = [permissions.AllowAny, ]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })
