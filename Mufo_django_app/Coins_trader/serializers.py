from rest_framework import serializers
from .models import Coins_trader


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins_trader
        fields = ('Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','Coins_Club_Owner_Id','Coins_Club_Owner_Phone_Number','Coins_Clubs_Owner_Email_id','National_ID','Pan_Card','Bank_Acc_Details','UPI_Address','Paytm_Address',)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model =Coins_trader
        fields =('phone',)

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model =Coins_trader
        fields =('otp',)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins_trader
        fields = ('Name','email','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','phone')
