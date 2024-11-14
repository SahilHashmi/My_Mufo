# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render, redirect
# from rest_framework import viewsets
# from datetime import datetime, timedelta
# from rest_framework.response import Response

# from .permissions import RoomPermission
# from . import serializers
# from .models import Room, Chat

# from User import serializers as public_serializer
# from django.shortcuts import get_object_or_404

# import html

# class RoomViewSets(viewsets.ModelViewSet):
    
#     serializer_class = serializers.RoomSerializer
#     queryset = Room.objects.filter(is_public=1).all()
#     lookup_field = "room_code"
#     permission_classes = [RoomPermission]


#     def perform_create(self, serializer):
#         room_name = serializer.validated_data.get('room_name')
        
#         serializer.save(creator=self.request.user)
#         serializer.save(room_name=html.escape(room_name))

#         return serializer
    
#     def create(self, request, *args, **kwargs):
#         instance = super().create(request, *args, **kwargs)
#         return Response(
#             {
#                 "status":"success", 
#                 "room_code":instance.data.get('room_code')
#             }
#         )

#     def retrieve(self, request, *args, **kwargs):
#         lookup_field = self.lookup_field or self.lookup_url_kwarg

#         lookup_kwargs = {lookup_field: self.kwargs[lookup_field]}
#         _ = get_object_or_404(Room, **lookup_kwargs)

#         queryset = Chat.objects.filter(room__room_code=self.kwargs[lookup_field], 
#                                        created__range=(datetime.now() - timedelta(days=5), datetime.now()))
#         serializer = serializers.ChatSerializer(queryset, many=True)
#         return Response(serializer.data)

# def profile(request):
#     serializer = public_serializer.UserSerializer
#     return render(request, 'chat/profile.html', {'serializer':serializer})

# def create_room(request):
#     return render(request, 'chat/create-room.html')

# class ChatViewSets(viewsets.ModelViewSet):
#     serializer_class = serializers.ChatSerializer
#     queryset = Chat.objects.all()
        
# def join_room(request, room_code):
#     is_exist = Room.objects.filter(room_code=room_code).first()
#     if not is_exist:
#         return redirect('chat:index_chat')
#     return render(request, 'chat/chat.html', context={'room_name':room_code})

# def index_chat(request):

#     return render(request, 'chat/index.html')


# views.py

from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from datetime import datetime, timedelta
from rest_framework.response import Response

from .permissions import RoomPermission
from . import serializers
from .models import Room, Chat

# from apps.public import serializers as public_serializer
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from Mufo.Minxins import authenticate_token
import html
from rest_framework.views import APIView


class RoomViewSets(viewsets.ModelViewSet):
    serializer_class = serializers.RoomSerializer
    queryset = Room.objects.all()
    lookup_field = "room_code"
    @method_decorator(authenticate_token)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        room_name = serializer.validated_data.get('room_name')
        serializer.save(creator=request.user)  # Use the authenticated user
        serializer.save(room_name=html.escape(room_name))
        return Response(
            {
                "status": "success",
                "room_code": serializer.data.get('room_code')
            },
            status=status.HTTP_201_CREATED
        )
    def retrieve(self, request, *args, **kwargs):
        lookup_field = self.lookup_field or self.lookup_url_kwarg

        lookup_kwargs = {lookup_field: self.kwargs[lookup_field]}
        _ = get_object_or_404(Room, **lookup_kwargs)

        queryset = Chat.objects.filter(room__room_code=self.kwargs[lookup_field],
                                       created__range=(datetime.now() - timedelta(days=5), datetime.now()))
        serializer = serializers.ChatSerializer(queryset, many=True)
        return Response(serializer.data)






class ChatViewSets(viewsets.ModelViewSet):

    serializer_class = serializers.ChatSerializer
    queryset = Chat.objects.all()


class JoinRoomView(APIView):
    def get(self, request, room_code):
        is_exist = Room.objects.filter(room_code=room_code).first()
        if not is_exist:
            return Response({"detail": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"room_name": room_code}, status=status.HTTP_200_OK)


class AllRoomView(APIView):
    def get(self,request):
        Rooms= Room.objects.filter(is_public=1)
        serializer = serializers.RoomsGetSerializer(Rooms,many=True)
        return Response(serializer.data)
    

class AllRoomofjockey(APIView):
    @method_decorator(authenticate_token)
    def get(self,request):
        Rooms= Room.objects.filter(creator=request.user.id)
        serializer = serializers.RoomsGetSerializer(Rooms,many=True)
        return Response(serializer.data)