from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from Mufo.Minxins import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, response
import random
from django.utils import timezone
from datetime import timedelta

from django.utils import timezone
from datetime import timedelta

from .models import User
from Audio_Jockey.models import Audio_Jockey
from Coins_club_owner.models import Coins_club_owner
from Coins_trader.models import Coins_trader
from Jockey_club_owner.models import Jockey_club_owner
import secrets
from django.utils.decorators import method_decorator
from Mufo.Minxins import authenticate_token
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework import filters
from master.serializers import *
from master.models import *
import uuid

def Users(request):
    return HttpResponse("Hello, world. You're at the User index.")


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

            email_exists = Audio_Jockey.objects.filter(email=email).exists()
            phone_number_exists = Audio_Jockey.objects.filter(
                phone=phone).exists()

            if email_exists or phone_number_exists:
                message = 'Email already exists as an Audio_Jockey ' if email_exists else 'Phone number already exists as an Audio_Jockey '
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
            usertype="User"
            serializer.save(token =token,uid=uid,usertype=usertype)
            if serializer1.is_valid():
                serializer1.save(token =token,uid=uid,usertype=usertype)
            return Response({'data': str(serializer.data), 'access': str(token), 'message': "Register successfully"}, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        phone = serializer.initial_data.get('phone')

        # Check if the phone number exists in any of the profile models
        profiles = [Audio_Jockey, Coins_club_owner,
                    Coins_trader, Jockey_club_owner, User]
        profile = None

        for profile_model in profiles:
            profile = profile_model.objects.filter(phone=phone).first()
            if profile:
                break

        if not profile:
            return Response({'message': "No user found with this mobile"}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(profile, 'Is_Approved') and not profile.Is_Approved:
            return Response({'message': f"{profile.__class__.__name__} {profile} is not approved Yet. Please wait for some time to get approved."}, status=status.HTTP_403_FORBIDDEN)

        user = profile.__class__.objects.get(phone=phone)
        current_time = timezone.now()
        if user.Otpcreated_at and user.Otpcreated_at > current_time:
            user.otp = random.randint(1000, 9999)
            user.Otpcreated_at = current_time + timedelta(minutes=5)
        else:
            user.otp = random.randint(1000, 9999)
            user.Otpcreated_at = current_time + timedelta(minutes=5)

        user.save()
        # send_otp_on_phone(phone, user.otp)
        return Response({'uid': str(user.uid), 'otp': str(user.otp), 'message': "Otp sent successfully"})


class Otp(APIView):
    serializer_class = OtpSerializer

    def post(self, request, uid):
        serializer = self.serializer_class(data=request.data)
        otp = serializer.initial_data.get('otp')
        profiles = [Audio_Jockey, Coins_club_owner,
                    Coins_trader, Jockey_club_owner, User]
        profile = None

        for profile_model in profiles:
            try:
                profile = profile_model.objects.get(uid=uid)
                break
            except profile_model.DoesNotExist:
                continue

        current_time = timezone.now()
        if otp == profile.otp and profile.Otpcreated_at and profile.Otpcreated_at > current_time:
            user_serializer = UserSerializer(profile)
            return Response({'data': {'data': (user_serializer.data), 'profile': (profile.__class__.__name__), 'id': (profile.id),  'access': str(profile.token), 'message': "Login successfully"}})
        else:
            return Response({'message': "Invalid OTP. Please try again"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, format=None):
        pk = request.user.uid
        user = User.objects.get(uid=pk)
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)

    @method_decorator(authenticate_token)
    def put(self, request, format=None):
        uid = request.user.uid
        user = get_object_or_404(User, uid=uid)
        common_objects = Common.objects.get(uid=uid)
        serializer = UserUpdateSerializer(user, data=request.data)
        serializer1 = masterUpdateSerializer(common_objects, data=request.data)
        if common_objects:
            serializer1 = masterUpdateSerializer(common_objects, data=request.data)
            if serializer1.is_valid():
                serializer1.save()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @method_decorator(authenticate_token)
    def delete(self, request, format=None):
        pk = request.user.uid
        user = User.objects.get(uid=pk)
        commonuser = Common.objects.get(uid=pk)
        if commonuser:
            commonuser.delete()
            user.delete()
            return Response({"delete":"successfully"})
        return Response({"delete":"unsuccessfully"})
    
class GetUserdata(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = GetUserSerializer(user)
            user_data = serializer.data
            user_data['is_followed'] = self.is_followed(user, request.user)
            user_data['follower_count'] = self.get_follower_count(user)
            user_data['following_count'] = self.get_following_count(user)
            return Response(user_data)
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def is_followed(self, user, current_user):
        return Follow.objects.filter(user=current_user, following_user=user).exists()

    def get_follower_count(self, user):
        return Follow.objects.filter(following_user=user).count()

    def get_following_count(self, user):
        return Follow.objects.filter(user=user).count()


class Searchalluser(ListAPIView):
    serializer_class = UserSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['Name', 'email']

    @method_decorator(authenticate_token)
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = User.objects.exclude(id=self.request.user.id)
        user = self.request.user
        if user:
            queryset = self.annotate_following(queryset, user)
        return queryset

    def annotate_following(self, queryset, user):
        for user_obj in queryset:
            user_obj.is_following = Follow.objects.filter(
                user=user, following_user=user_obj).exists()
        return queryset


class GetUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, Userid):
        try:
            user = User.objects.get(id=Userid)
            serializer = GetUserSerializer(user)
            user_data = serializer.data
            user_data['is_followed'] = self.is_followed(user, request.user)
            user_data['follower_count'] = self.get_follower_count(user)
            user_data['following_count'] = self.get_following_count(user)
            return Response(user_data)
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def is_followed(self, user, current_user):
        return Follow.objects.filter(user=current_user, following_user=user).exists()

    def get_follower_count(self, user):
        return Follow.objects.filter(following_user=user).count()

    def get_following_count(self, user):
        return Follow.objects.filter(user=user).count()


class FollowUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, follow):
        try:
            following_user = User.objects.get(id=follow)
            follow_user, created = Follow.objects.get_or_create(
                user=request.user, following_user=following_user)

            if not created:
                follow_user.delete()
                return Response({'success': True, 'message': 'Unfollowed user'})
            else:
                return Response({'success': True, 'message': 'Followed user'})

        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'})


class FollowerList(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        user = request.user  
        followers = Follow.objects.filter(following_user=user)
        followed_users = Follow.objects.filter(user=user, following_user__in=followers.values_list('user', flat=True))
        
        queryset = self.annotate_followers(followers, followed_users)
        serializer = getfollowerSerializer(queryset, many=True)
        
        return Response(serializer.data)

    def annotate_followers(self, followers, followed_users):
        user_dict = {}
        followed_users_set = set(followed_users.values_list('following_user', flat=True))
        
        for follower in followers:
            following_user = follower.user
            user_dict[following_user.id] = {
                "id": following_user.id,
                "Name": following_user.Name,
                "email": following_user.email,
                "Gender": following_user.Gender,
                "Dob": following_user.Dob,
                "profile_picture": following_user.profile_picture,
                "Introduction_voice": following_user.Introduction_voice,
                "Introduction_text": following_user.Introduction_text,
                "is_followed": following_user.id in followed_users_set
            }
        
        return list(user_dict.values())


class FollowingList(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, *args, **kwargs):
        following = Follow.objects.filter(user=request.user)
        followed_users = [follow_obj.following_user for follow_obj in following]

        user_data_list = []
        for user in followed_users:
            user_data = {
                "id": user.id,
                "Name": user.Name,
                "email": user.email,
                "Gender": user.Gender,
                "Dob": user.Dob,
                "profile_picture": user.profile_picture,
                "Introduction_voice": user.Introduction_voice,
                "Introduction_text": user.Introduction_text,
                "is_followed": True  
            }
            user_data_list.append(user_data)

        return Response(user_data_list)


@method_decorator(authenticate_token, name='dispatch')
class userview(APIView):
    def get(self, request):
        user = request.user
        print(user)
        return JsonResponse({'uid': user.uid, 'number': user.phone, "name": user.Name})
    
class Alluser(APIView):
    def get(self,request):
        data=User.objects.all()
        serialiser = UserSerializer(data,many=True)
        return Response(serialiser.data)
