from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path("", views.coins_club_owner, name="index"),
    path("Register/", Register.as_view(), name="Register"),
    path('Updateuser/', UpdateUser.as_view(), name="Updateuser"),
    path("getallcointrader/", CointraderList.as_view(), name="getallcointrader"),
    path('userview/', userview.as_view(), name="userview"),
    path('allcoinclubowner/', Alluser.as_view(), name="userview"),
]
