from rest_framework import serializers
from .models import Coins_club_owner


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins_club_owner
        fields = ('Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','National_ID','Pan_Card','Bank_Acc_Details','UPI_Address','Paytm_Address',)

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model =Coins_club_owner
        fields =('phone',)

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model =Coins_club_owner
        fields =('otp',)



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins_club_owner
        fields = ('Name','email','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','phone')
