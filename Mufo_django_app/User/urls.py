from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from .views import *

urlpatterns = [
    path("", views.Users, name="User"),
    path("Register/", Register.as_view(), name="Register"),
    path('login/', Login.as_view(), name="login"),
    path('otp/<uid>/', Otp.as_view() , name='otp'),
    path('getUserData/', GetUserdata.as_view(), name="GetUserdata"),
    path('Updateuser/', UpdateUser.as_view(), name="Updateuser"),
    path('Searchalluser/', Searchalluser.as_view(), name="userview"),
    path('getUser/<int:Userid>/', GetUser.as_view(), name='getUser'),
    path('follow/<int:follow>/', FollowUser.as_view(), name='follow-user'),
    path('followers/', FollowerList.as_view(), name='follower-list'),
    path('following/', FollowingList.as_view(), name='following-list'),
    path('userview/', userview.as_view(), name="userview"),
    path('alluser/', Alluser.as_view(), name="userview"),
]
