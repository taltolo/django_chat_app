from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from .serializers import MessageSerializer
from .models import Message,User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . import serializers
from .utils import get_and_authenticate_user
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import mixins

class userViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
   

    # @action(methods=['POST', ], detail=False,)
    # def login(self, request):
    #     print(self.queryset)
    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer)
    #     serializer.is_valid(raise_exception=True)
    #     user = get_and_authenticate_user(**serializer.validated_data)
    #     print(user)
    #     data = serializers.AuthUserSerializer(user).data
    #     print(data)
    #     return Response(data=data, status=status.HTTP_200_OK)

    # def get_serializer_class(self):
    #     if not isinstance(self.serializer_classes, dict):
    #         raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

    #     if self.action in self.serializer_classes.keys():
    #         return self.serializer_classes[self.action]
    #     return super().get_serializer_class()



class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        return serializer.save(sender=self.request.user)

    def create_message(self,request):
        print(request.user)
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    # def perform_destroy(self, serializer):
    #     return serializer.delete(id=self.messageToDelete)

    @action(methods=['delete', ], detail=True)
    def destroy_message(self,request,pk):
        try:
            print(request.data)
            messageToDelete = Message.objects.get(id=pk)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        messageToDelete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', ], detail=True)
    def read_message(self,request, pk):
        try:
            messageDisplay = Message.objects.get(id=pk)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            messageDisplay.unread=False
            messageDisplay.save()
        serializer = MessageSerializer(messageDisplay)
        return Response(serializer.data)

    @action(methods=['GET', ], detail=False)
    def get_messages_by_user(self,request):
        try:
            print(request.user)
            messagesDisplay=Message.objects.filter(receiver=request.user)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(messagesDisplay, many=True)
        return Response(serializer.data)

    @action(methods=['GET', ], detail=False)
    def get_unread_messages(self,request):
        try:
            print(self.queryset)
            print(request.data)
            messagesDisplay =self.queryset.filter(receiver=request.user).filter(unread=True)
            print(messagesDisplay)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(messagesDisplay, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
class CustomAuthToken(ObtainAuthToken):
    permission_classes = [permissions.AllowAny, ]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })
