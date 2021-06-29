from django.urls import path,include
from rest_framework import routers
from . import views
from django.contrib import admin



router = routers.DefaultRouter()
router.register('user', views.userViewSet)
router.register('message', views.MessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', views.login.as_view()),
]
