
from django.http import HttpResponse,JsonResponse
# from .Mixins import *
from Mufo.Minxins import *
from .serializers import *
from .models import Audio_Jockey
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, response
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages

from django.utils import timezone
from datetime import timedelta

from User.models import User
from Coins_club_owner.models import Coins_club_owner
from Coins_trader.models import Coins_trader
from Jockey_club_owner.models import Jockey_club_owner

import random


from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import secrets

from django.utils.decorators import method_decorator
from master.serializers import *
import uuid
from django.shortcuts import get_object_or_404

def audio_jockey(request):
    return HttpResponse("Hello, world. You're at the Audio_jockey index.")


from Mufo.Minxins import authenticate_token

class Register(APIView):
    serializer_class = UserSerializer
    serializer_class1 = masterSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer1 = self.serializer_class1(data=request.data)
        phone = serializer.initial_data.get('phone')
        email = serializer.initial_data.get('email')
        if serializer.is_valid():

            email_exists = User.objects.filter(email=email).exists()
            phone_number_exists = User.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an users ' if email_exists else 'Phone number already exists as an users '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            email_exists = Coins_club_owner.objects.filter(
                email=email).exists()
            phone_number_exists = Coins_club_owner.objects.filter(
                phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as coin club owner ' if email_exists else 'Phone number already exists as coin club owner'
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            email_exists = Coins_trader.objects.filter(email=email).exists()
            phone_number_exists = Coins_trader.objects.filter(
                phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Coins_trader ' if email_exists else 'Phone number already exists as an Coins_trader '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            email_exists = Jockey_club_owner.objects.filter(
                email=email).exists()
            phone_number_exists = Jockey_club_owner.objects.filter(
                phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Jockey_club_owner ' if email_exists else 'Phone number already exists as an Jockey_club_owner '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            token = secrets.token_hex(128)
            uid = uuid.uuid1()
            usertype="Audio_Jockey"
            serializer.save(token =token,uid=uid,usertype=usertype)
            if serializer1.is_valid():
                serializer1.save(token =token,uid=uid,usertype=usertype)
            user = Audio_Jockey.objects.get(email=serializer.data['email'])
            messages.add_message(
                request, messages.INFO, f"New Audio jockey {user} is registered. please Approve ")
            return Response({'message': "Register successfully. Please wait for some time to Get Approved."}, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(authenticate_token, name='dispatch')
class AudioJockeyConnectedOwner(APIView):
    def get(self, request):
        try:
            user = request.user.id
            audio_jockey = Audio_Jockey.objects.get(id=user)
            connected_owner = audio_jockey.Club_Owner_Id
            if connected_owner:
                owner_data = {
                    'id': connected_owner.id,
                    'name': connected_owner.Name,
                    'email': connected_owner.email,
                    'image':connected_owner.profile_picture
                }
                return Response(owner_data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No connected Jockey Club Owner found'}, status=status.HTTP_404_NOT_FOUND)
        except Audio_Jockey.DoesNotExist:
            return Response({'message': 'Audio Jockey not found'}, status=status.HTTP_404_NOT_FOUND)






@method_decorator(authenticate_token, name='dispatch')
class userview(APIView):

    def get(self, request):
        user = request.user
        print(user)
        return JsonResponse({'uid': user.uid, 'number': user.phone,"name":user.Name})
    

class UpdateUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, format=None):
        pk = request.user.uid
        user = Audio_Jockey.objects.get(uid=pk)
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)
    @method_decorator(authenticate_token)
    def put(self, request,format=None):
        pk = request.user.uid
        user = Audio_Jockey.objects.get(uid=pk)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    @method_decorator(authenticate_token)
    def delete(self, request, format=None):
        pk = request.user.uid
        user = Audio_Jockey.objects.get(uid=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# class UpdateUser(APIView):
#     @method_decorator(authenticate_token)
#     def get(self, request, format=None):
#         pk = request.user.uid
#         user = Audio_Jockey.objects.get(uid=pk)
#         serializer = UserUpdateSerializer(user)
#         return Response(serializer.data)

#     @method_decorator(authenticate_token)
#     def put(self, request, format=None):
#         uid = request.user.uid
#         print(uid)
#         user = get_object_or_404(Audio_Jockey, uid=uid)
#         print(user)
#         common_objects = Common.objects.get(uid=uid)
#         print(common_objects)
#         serializer = UserUpdateSerializer(user, data=request.data)
#         serializer1 = masterUpdateSerializer(common_objects, data=request.data)
#         if common_objects:
#             serializer1 = masterUpdateSerializer(common_objects, data=request.data)
#             if serializer1.is_valid():
#                 serializer1.save()                
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
#     @method_decorator(authenticate_token)
#     def delete(self, request, format=None):
#         pk = request.user.uid
#         print(pk)
#         user = Audio_Jockey.objects.get(uid=pk)
#         print(user)
#         commonuser = Common.objects.get(uid=pk)
#         print(commonuser)
#         if commonuser:
#             commonuser.delete()
#             user.delete()
#             return Response({"delete":"successfully"})
#         return Response({"delete":"unsuccessfully"})

class Alluser(APIView):
    def get(self, request):
        data = Audio_Jockey.objects.all()
        approved_users = []
        for user in data:
            if user.Is_Approved:
                approved_users.append(user)
        if approved_users:
            serializer = UserSerializer(approved_users, many=True)
            return Response(serializer.data)
        return Response("No approved users found")