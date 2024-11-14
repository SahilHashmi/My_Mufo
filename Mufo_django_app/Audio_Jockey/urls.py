from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", views.audio_jockey, name="index"),
    path("Register/", Register.as_view(), name="Register"),
    path('Updateuser/', UpdateUser.as_view(), name="Updateuser"),
    path("getjockey_owner/", AudioJockeyConnectedOwner.as_view(), name="getjockey_owner"),
    path('userview/', userview.as_view(), name="userview"),
    path('allcoinclubowner/', Alluser.as_view(), name="userview"),
    path('allaudiojockeyuser/', Alluser.as_view(), name="userview"),
]
