from django.urls import path,include
from rest_framework import routers
from . import views
from django.contrib import admin



router = routers.DefaultRouter()
router.register(r'user', views.userViewSet)
router.register(r'message', views.MessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.CustomAuthToken.as_view()),
]
