from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", views.coins_trader, name="coins_trader"),
    path("Register/", Register.as_view(), name="Register"),
    path('Updateuser/', UpdateUser.as_view(), name="Updateuser"),
    path("getcoin_club_owner/", CointraderConnectedOwner.as_view(), name="getcoin_club_owner"),
    path('userview/', userview.as_view(), name="userview"),
    path('allcointrader/', Alluser.as_view(), name="userview"),
]
