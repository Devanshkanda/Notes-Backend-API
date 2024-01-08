from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'auth', viewset=User_Login_And_SignUp_Viewset, basename="user signup")
router.register(r'notes', viewset=NotesViewSet, basename="notes")


urlpatterns = [
    path('', include(router.urls)),
]