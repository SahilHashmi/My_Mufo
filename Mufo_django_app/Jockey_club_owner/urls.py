from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("", views.Jockey_club_owners, name="Jockey_club_owner"),
    path("Register/", Register.as_view(), name="Register"),
    path('Updateuser/', UpdateUser.as_view(), name="Updateuser"),
    path("getallaudiojockey/", AudioJockeyList.as_view(), name="getallaudiojockey"),
    path("userview/", userview.as_view(), name="userview"),
    path('alljockeyuser/', Alluser.as_view(), name="userview"),

]
