from rest_framework import serializers
from .models import*


class clubownerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Admin_to_Coins_club_owner
        fields=['Coins_Club_Owner_Id','numcoin','created_date']



class CointraderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coins_club_owner_to_Coins_trader
        fields = ['to_trader','amount','created_date']




class Jockey_club_ownerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins_trader_to_Jockey_club_owner
        fields = ['to_Jockey_club_owner','amount','created_date']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins_trader_to_User
        fields = ['to_User','amount','created_date']


class Audio_JockeySerializer(serializers.ModelSerializer):
    class Meta:
        model = User_to_Audio_Jockey
        fields = ['to_Audio_Jockey','amount','created_date']



# transaction history serializer

class clubowner1Serializer(serializers.ModelSerializer):
    Coins_Club_Owner_Id = serializers.SerializerMethodField()

    def get_Coins_Club_Owner_Id(self, obj):
        return obj.Coins_Club_Owner_Id.Name

    class Meta:
        model = Admin_to_Coins_club_owner
        fields=['Coins_Club_Owner_Id','numcoin','created_date']


class Cointrader1Serializer(serializers.ModelSerializer):
    to_trader = serializers.SerializerMethodField()

    def get_to_trader(self, obj):
        return obj.to_trader.Name
    class Meta:
        model = Coins_club_owner_to_Coins_trader
        fields = ['to_trader','amount','created_date']

class Jockey_club_owner1Serializer(serializers.ModelSerializer):
    to_Jockey_club_owner = serializers.SerializerMethodField()

    def get_to_Jockey_club_owner(self, obj):
        return obj.to_Jockey_club_owner.Name
    class Meta:
        model = Coins_trader_to_Jockey_club_owner
        fields = ['to_Jockey_club_owner','amount','created_date']

class User1Serializer(serializers.ModelSerializer):
    to_User = serializers.SerializerMethodField()

    def get_to_User(self, obj):
        return obj.to_User.Name
    class Meta:
        model = Coins_trader_to_User
        fields = ['to_User','amount','created_date']

class Audio_Jockey1Serializer(serializers.ModelSerializer):
    to_Audio_Jockey = serializers.SerializerMethodField()

    def get_to_Audio_Jockey(self, obj):
        return obj.to_Audio_Jockey.Name
    class Meta:
        model = User_to_Audio_Jockey
        fields = ['to_Audio_Jockey','amount','created_date']

