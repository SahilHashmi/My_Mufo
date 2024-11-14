from rest_framework import serializers
from master.models import *

class masterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common
        fields = '__all__'


class masterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common
        fields = ('Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text',)

        



class FollowerSerializer(serializers.ModelSerializer):
    user = masterSerializer()

    class Meta:
        model = Follow1
        fields = ('user', 'created_at')


class FollowingSerializer(serializers.ModelSerializer):
    following_user = masterSerializer()

    class Meta:
        model = Follow1
        fields = ('following_user', 'created_at')


class getfollowerSerializer(serializers.ModelSerializer):
    is_followed = serializers.BooleanField(default=False)

    class Meta:
        model = Common
        fields = ('id','Name', 'email', 'Gender', 'Dob', 'profile_picture', 'Introduction_voice', 'Introduction_text', 'is_followed')


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common
        fields = ('id','Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','coins',)

class UserSearchSerializer(serializers.ModelSerializer):
    is_following = serializers.BooleanField(read_only=True)
    class Meta:
        model = Common
        fields = ('id','Name','email','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','is_following',)