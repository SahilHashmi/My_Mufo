# from django.urls import path

# from . import views

# app_name = 'chat'

# urlpatterns = [
#     path('room/<str:room_code>', views.join_room, name='join_room'),
#     path('create-room', views.create_room, name='create_room'),
#     path('', views.index_chat, name='index_chat')
# ]
# urls.py

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# app_name = 'chat'

# router = DefaultRouter()
# router.register(r'rooms', views.RoomViewSets, basename='room')
# router.register(r'chats', views.ChatViewSets, basename='chat')

# urlpatterns = [
#     path('room/<str:room_code>/', views.join_room, name='join_room'),
#     path('create-room/', views.create_room, name='create_room'),
#     path('api/', include(router.urls)),
# ]

# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# app_name = 'chat'

# router = DefaultRouter()
# router.register(r'rooms', views.RoomViewSets, basename='room')
# router.register(r'chats', views.ChatViewSets, basename='chat')

urlpatterns = [
    path('room/<str:room_code>/', views.JoinRoomView.as_view(), name='join_room'),
    path('create-room/', views.RoomViewSets.as_view({'post': 'create'}), name='create_room'),
    path('rooms/', views.AllRoomView.as_view(), name='rooms'),
    path('jockeyroom/', views.AllRoomofjockey.as_view(), name='jockeyroom'),
]
