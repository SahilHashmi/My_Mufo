from rest_framework import serializers
from .models import Audio_Jockey


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio_Jockey
        fields = ('Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','Club_Owner_Id','Club_Owner_Phone_Number','Club_Owner_Email_id','National_ID','Pan_Card','Bank_Acc_Details','UPI_Address','Paytm_Address',)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model =Audio_Jockey
        fields =('phone',)

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model =Audio_Jockey
        fields =('otp',)



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio_Jockey
        fields = ('Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text')