
from django.http import HttpResponse,JsonResponse
from Mufo.Minxins import *
from .serializers import *
from .models import Coins_club_owner 
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status, response
from django.contrib import messages

from Audio_Jockey.models import Audio_Jockey
from User.models import User
from Coins_trader.models import Coins_trader
from Jockey_club_owner.models import Jockey_club_owner
import secrets
from django.utils.decorators import method_decorator
from Mufo.Minxins import authenticate_token
from master.serializers import *
import uuid
def coins_club_owner(request):
    return HttpResponse("Hello, world. You're at the Coins_club_owner index.")


class Register(APIView):
    serializer_class = UserSerializer
    serializer_class1 = masterSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer1 = self.serializer_class1(data=request.data)

        phone=serializer.initial_data.get('phone')
        email=serializer.initial_data.get('email')
        if serializer.is_valid():

            email_exists = Audio_Jockey.objects.filter(email=email).exists()
            phone_number_exists = Audio_Jockey.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Audio_Jockey ' if email_exists else 'Phone number already exists as an Audio_Jockey '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            email_exists = User.objects.filter(email=email).exists()
            phone_number_exists = User.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as User ' if email_exists else 'Phone number already exists as User'
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
            
            email_exists = Coins_trader.objects.filter(email=email).exists()
            phone_number_exists = Coins_trader.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Coins_trader ' if email_exists else 'Phone number already exists as an Coins_trader '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


            email_exists = Jockey_club_owner.objects.filter(email=email).exists()
            phone_number_exists = Jockey_club_owner.objects.filter(phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Jockey_club_owner ' if email_exists else 'Phone number already exists as an Jockey_club_owner '
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            token = secrets.token_hex(128)
            uid = uuid.uuid1()
            usertype="Coins_club_owner"
            serializer.save(token =token,uid=uid,usertype=usertype)
            if serializer1.is_valid():
                serializer1.save(token =token,uid=uid,usertype=usertype)
            user = Coins_club_owner.objects.get(email=serializer.data['email'])
            messages.add_message(request, messages.INFO, f"New coins club owner {user} is registered. please Approve ")
            return Response({'message': "Register successfully. Please wait for some time to Get Approved."}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(authenticate_token, name='dispatch')
class CointraderList(APIView):
    def get(self, request):
        try:
            user = request.user.id
            coin_traders = Coins_trader.objects.filter(Coins_Club_Owner_Id=user,Is_Approved=True)
            coin_trader_data = []
            for coin_trader in coin_traders:
                coin_trader_data.append({
                    'id': coin_trader.id,
                    'name': coin_trader.Name,
                    'email': coin_trader.email,
                    'image':coin_trader.profile_picture
                })
            return Response(coin_trader_data, status=status.HTTP_200_OK)
        except Jockey_club_owner.DoesNotExist:
            return Response({'message': 'Coin Club Owner not found'}, status=status.HTTP_404_NOT_FOUND)



class UpdateUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, format=None):
        pk = request.user.uid
        user = Coins_club_owner.objects.get(uid=pk)
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)
    @method_decorator(authenticate_token)
    def put(self, request,format=None):
        pk = request.user.uid
        user = Coins_club_owner.objects.get(uid=pk)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    @method_decorator(authenticate_token)
    def delete(self, request, format=None):
        pk = request.user.uid
        user = Coins_club_owner.objects.get(uid=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class UpdateUser(APIView):
#     @method_decorator(authenticate_token)
#     def get(self, request, format=None):
#         pk = request.user.uid
#         user = Coins_club_owner.objects.get(uid=pk)
#         serializer = UserUpdateSerializer(user)
#         return Response(serializer.data)

#     @method_decorator(authenticate_token)
#     def put(self, request, format=None):
#         uid = request.user.uid
#         print(uid)
#         user = Coins_club_owner.objects.get(uid=uid)
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
#         user = Coins_club_owner.objects.get(uid=pk)
#         print(user)
#         commonuser = Common.objects.get(uid=pk)
#         print(commonuser)
#         if commonuser:
#             commonuser.delete()
#             user.delete()
#             return Response({"delete":"successfully"})
#         return Response({"delete":"unsuccessfully"})

@method_decorator(authenticate_token, name='dispatch')
class userview(APIView):

    def get(self, request):
        user = request.user
        print(user)
        return JsonResponse({'uid': user.uid, 'number': user.phone,"name":user.Name})
    

class Alluser(APIView):
    def get(self, request):
        data = Coins_club_owner.objects.all()
        approved_users = []
        for user in data:
            if user.Is_Approved:
                approved_users.append(user)
        if approved_users:
            serializer = UserSerializer(approved_users, many=True)
            return Response(serializer.data)
        return Response("No approved users found")