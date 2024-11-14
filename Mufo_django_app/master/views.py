from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from Mufo.Minxins import authenticate_token
from master.models import *
from .serializers import *
from rest_framework import status, response
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework import filters

class FollowUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, follow):
        try:
            following_common = Common.objects.get(uid=follow)  # Rename variable

            print("Following User:", following_common)  # Debugging print
            print("Request User:", request.user)       # Debugging print

            # Rename the variable to avoid conflict
            follow_user, created = Follow1.objects.get_or_create(user=request.user, following_user=following_common)

            print("Follow User:", follow_user)
            
            if not created:
                follow_user.delete()
                return Response({'success': True, 'message': 'Unfollowed user'})
            else:
                return Response({'success': True, 'message': 'Followed user'})
            # return Response({'success': False, 'message': 'User does not exist.'})
        except Common.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'})

    
class FollowerList(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        user = request.user  
        followers = Follow1.objects.filter(following_user=user)
        followed_users = Follow1.objects.filter(user=user, following_user__in=followers.values_list('user', flat=True))
        
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
        following = Follow1.objects.filter(user=request.user)
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


class GetUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, Userid):
        try:
            user = Common.objects.get(uid=Userid)
            serializer = GetUserSerializer(user)
            user_data = serializer.data
            user_data['is_followed'] = self.is_followed(user, request.user)
            user_data['follower_count'] = self.get_follower_count(user)
            user_data['following_count'] = self.get_following_count(user)
            return Response(user_data)
        except Common.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def is_followed(self, user, current_user):
        return Follow1.objects.filter(user=current_user, following_user=user).exists()

    def get_follower_count(self, user):
        return Follow1.objects.filter(following_user=user).count()

    def get_following_count(self, user):
        return Follow1.objects.filter(user=user).count()
    

class GetUserdata(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        try:
            user = Common.objects.get(uid=request.user.uid)
            serializer = GetUserSerializer(user)
            user_data = serializer.data
            user_data['is_followed'] = self.is_followed(user, request.user)
            user_data['follower_count'] = self.get_follower_count(user)
            user_data['following_count'] = self.get_following_count(user)
            return Response(user_data)
        except Common.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def is_followed(self, user, current_user):
        return Follow1.objects.filter(user=current_user, following_user=user).exists()

    def get_follower_count(self, user):
        return Follow1.objects.filter(following_user=user).count()

    def get_following_count(self, user):
        return Follow1.objects.filter(user=user).count()
    

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
        queryset = Common.objects.exclude(id=self.request.user.id)
        user = self.request.user
        verifide = user.is_verifide=True
        if user:
            queryset = self.annotate_following(queryset, user)
        return queryset

    def annotate_following(self, queryset, user):
        for user_obj in queryset:
            user_obj.is_following = Follow1.objects.filter(
                user=user, following_user=user_obj).exists()
        return queryset

class Alluser(APIView):
    def get(self, request):
        data=Common.objects.all()
        serialiser = masterSerializer(data,many=True)
        return Response(serialiser.data)