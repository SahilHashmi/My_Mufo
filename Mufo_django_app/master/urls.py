from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from . import views
from .views import *

urlpatterns = [
    path('follow/<uuid:follow>/', FollowUser.as_view(), name='follow-user'),
    path('followers/', FollowerList.as_view(), name='follower-list'),
    path('following/', FollowingList.as_view(), name='following-list'),
    path('getUser/<uuid:Userid>/', GetUser.as_view(), name='getUser'),
    path('getUserData/', GetUserdata.as_view(), name="GetUserdata"),
    path('Searchalluser/', Searchalluser.as_view(), name="userview"),
    path('allcommonuser/', Alluser.as_view(), name="userview"),
]
