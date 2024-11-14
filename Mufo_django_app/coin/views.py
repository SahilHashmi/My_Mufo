from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, response
from .serializers import *
from Coins_club_owner.models import *
from Coins_trader.models import *
from django.utils.decorators import method_decorator
from Mufo.Minxins import authenticate_token
from datetime import datetime



class transfar1(APIView):
    sealizer_class = clubownerSerializer
    def post(self, request):
        serializer= self.sealizer_class(data=request.data)
        if serializer.is_valid():
            numcoin = serializer.validated_data.get('numcoin')
            owner_id = serializer.validated_data.get('Coins_Club_Owner_Id')
            try:
                club_owner = Coins_club_owner.objects.get(Name=owner_id)
                club_owner.coins += numcoin
                club_owner.save()
                transfer = Admin_to_Coins_club_owner.objects.create(Coins_Club_Owner_Id=club_owner, numcoin=numcoin,created_date=datetime.today())
                return Response({'total_coins': club_owner.coins,'message': 'Coins added successfully.'}, status=status.HTTP_201_CREATED)
            except Coins_club_owner.DoesNotExist:
                return Response({'error': 'Coins_club_owner matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            id=request.user.id
            club_owner = Coins_club_owner.objects.get(uid=request.user.uid)
            total_coins = club_owner.coins
            return Response({'total_coins': total_coins}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Please provide a valid club_owner.'}, status=status.HTTP_400_BAD_REQUEST)


class CoinTransfer2(APIView):
    serializer_class = CointraderSerializer
    @method_decorator(authenticate_token)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            trader_id = serializer.validated_data.get('to_trader')
            amount = serializer.validated_data.get('amount')
            try:
                owner = Coins_club_owner.objects.get(id=request.user.id)
                trader = Coins_trader.objects.get(Name=trader_id)
                owner_coins = owner.coins
                if owner_coins >= amount:
                    owner_coins -= amount
                    owner.coins = owner_coins
                    owner.save()
                    transfer = Coins_club_owner_to_Coins_trader.objects.create(from_owner=owner, to_trader=trader, amount=amount,created_date=datetime.today())
                    trader_coins = Coins_club_owner_to_Coins_trader.objects.filter(to_trader=trader).aggregate(total_coins=models.Sum('amount'))['total_coins']
                    if trader_coins is None:
                        trader_coins = 0
                    trader.coins = trader_coins
                    trader.save()
                    return Response({"total_coins": trader_coins, "message": "Coin transfer successful."}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Insufficient coins in the owner account.'}, status=status.HTTP_400_BAD_REQUEST)
            except Coins_club_owner.DoesNotExist:
                return Response({'error': 'Coins_club_owner matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            except Coins_trader.DoesNotExist:
                return Response({'error': 'Coins_trader matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            id=request.user.id
            trader = Coins_trader.objects.get(uid=request.user.uid)
            total_coins = trader.coins
            return Response({'total_coins': total_coins}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Please provide a valid Coins_trader Token.'}, status=status.HTTP_400_BAD_REQUEST)




class CoinTransfer3(APIView):
    serializer_class = Jockey_club_ownerSerializer
    @method_decorator(authenticate_token)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():  
            jockey_owner_id = serializer.validated_data.get('to_Jockey_club_owner')
            amount = serializer.validated_data.get('amount')
            try:
                trader = Coins_trader.objects.get(id=request.user.id)
                jockey_owner = Jockey_club_owner.objects.get(Name=jockey_owner_id)
                trader_coins = trader.coins
                if trader_coins >= amount:
                    trader_coins -= amount
                    trader.coins = trader_coins
                    trader.save()
                    transfer = Coins_trader_to_Jockey_club_owner.objects.create(from_trader=trader, to_Jockey_club_owner=jockey_owner, amount=amount,created_date=datetime.today())
                    jockey_owner_coins = Coins_trader_to_Jockey_club_owner.objects.filter(to_Jockey_club_owner=jockey_owner).aggregate(total_coins=models.Sum('amount'))['total_coins']
                    if jockey_owner_coins is None:
                        jockey_owner_coins = 0
                    jockey_owner.coins = jockey_owner_coins
                    jockey_owner.save()
                    return Response({"total coins":jockey_owner_coins,'message': 'Coin transfer successful.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Insufficient coins in the trader account.'}, status=status.HTTP_400_BAD_REQUEST)
            except Coins_trader.DoesNotExist:
                return Response({'error': 'Coins_trader matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            except Jockey_club_owner.DoesNotExist:
                return Response({'error': 'Jockey_club_owner matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            id=request.user.id
            jokyclubowner = Jockey_club_owner.objects.get(uid=request.user.uid)
            total_coins = jokyclubowner.coins
            return Response({'total_coins': total_coins}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Please provide a valid Jockey_club_owner Token.'}, status=status.HTTP_400_BAD_REQUEST)

class CoinTransfer31(APIView):
    serializer_class = UserSerializer
    @method_decorator(authenticate_token)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data.get('to_User')
            amount = serializer.validated_data.get('amount')
            try:
                trader = Coins_trader.objects.get(id=request.user.id)
                user = User.objects.get(Name=user_id)
                trader_coins = trader.coins
                if trader_coins >= amount:
                    trader_coins -= amount
                    trader.coins = trader_coins
                    trader.save()
                    transfer = Coins_trader_to_User.objects.create(from_trader=trader, to_User=user, amount=amount,created_date=datetime.today())
                    user_coins = Coins_trader_to_User.objects.filter(to_User=user).aggregate(total_coins=models.Sum('amount'))['total_coins']
                    if user_coins is None:
                        user_coins = 0
                    user.coins = user_coins
                    user.save()
                    return Response({"total coins":user_coins,'message': 'Coin transfer successful.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Insufficient coins in the trader account.'}, status=status.HTTP_400_BAD_REQUEST)
            except Coins_trader.DoesNotExist:
                return Response({'error': 'Coins_trader matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'user matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            id=request.user.id
            wallet = User.objects.get(uid=request.user.uid)
            total_coins = wallet.coins
            return Response({'total_coins': total_coins}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Please provide a valid User Token.'}, status=status.HTTP_400_BAD_REQUEST)

class CoinTransfer4(APIView):
    serializer_class = Audio_JockeySerializer
    @method_decorator(authenticate_token)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): 
            audio_jockey_id = serializer.validated_data.get('to_Audio_Jockey')
            amount = serializer.validated_data.get('amount')
            try:
                audio_jockey = Audio_Jockey.objects.get(Name=audio_jockey_id)
                user = User.objects.get(id=request.user.id)
                user_coins = user.coins
                if user_coins >= amount:
                    user_coins -= amount
                    user.coins = user_coins
                    user.save()
                    transfer = User_to_Audio_Jockey.objects.create(from_User=user, to_Audio_Jockey=audio_jockey, amount=amount,created_date=datetime.today())
                    audio_jockey_coins = User_to_Audio_Jockey.objects.filter(to_Audio_Jockey=audio_jockey).aggregate(total_coins=models.Sum('amount'))['total_coins']
                    if audio_jockey_coins is None:
                        audio_jockey_coins = 0
                    audio_jockey.coins = audio_jockey_coins
                    audio_jockey.save()
                    return Response({'total_coins': audio_jockey_coins,'message': 'Coin transfer successful.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Insufficient coins in the Jockey_club_owner account.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            except Audio_Jockey.DoesNotExist:
                return Response({'error': 'Audio_Jockey matching query does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            id=request.user.id
            wallet = Audio_Jockey.objects.get(uid=request.user.uid)
            total_coins = wallet.coins
            return Response({'total_coins': total_coins}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Please provide a valid Audio_Jockey ID.'}, status=status.HTTP_400_BAD_REQUEST)
# transaction history

class clubownerTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            user_id = request.user.id   
            club_owner = Coins_club_owner.objects.get(uid=request.user.uid)
            received_from_admin = Admin_to_Coins_club_owner.objects.filter(Coins_Club_Owner_Id=club_owner)
            sent_to_trader = Coins_club_owner_to_Coins_trader.objects.filter(from_owner=club_owner)
            all_transactions = list(received_from_admin) + list(sent_to_trader)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            for transaction in all_transactions:
                if isinstance(transaction, Admin_to_Coins_club_owner):     
                    serializer = clubowner1Serializer(transaction)
                    transaction_type = "Received from Admin"
                elif isinstance(transaction, Coins_club_owner_to_Coins_trader):  
                    serializer = Cointrader1Serializer(transaction)
                    transaction_type = "Paid to"
                else: 
                    continue
                data = serializer.data
                dict = {"transaction_type": transaction_type}
                dict.update(data)
                transaction_data.append(dict)
            return Response({"Transactions_History": transaction_data})
        except Coins_club_owner.DoesNotExist:
            return Response({'error': 'Club owner not found.'})
        except Admin_to_Coins_club_owner.DoesNotExist:
            return Response({'error': 'No transactions received from admin.'})
        except Coins_club_owner_to_Coins_trader.DoesNotExist:
            return Response({'error': 'No transactions sent to trader.'})
        except Exception as e:
            return Response({'error': 'Please provide a valid club_owner.'})
        

class cointraderTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            user_id = request.user.id   
            trader = Coins_trader.objects.get(uid=request.user.uid)
            received = Coins_club_owner_to_Coins_trader.objects.filter(to_trader=trader)
            sent_Jockey_club_owner = Coins_trader_to_Jockey_club_owner.objects.filter(from_trader=trader)
            sent_user = Coins_trader_to_User.objects.filter(from_trader=trader)

            all_transactions = list(received) + list(sent_Jockey_club_owner)+list(sent_user)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            for transaction in all_transactions:
                if isinstance(transaction, Coins_club_owner_to_Coins_trader):     
                    serializer = Cointrader1Serializer(transaction)
                    transaction_type = "Received from CoinClubowner"
                elif isinstance(transaction, Coins_trader_to_Jockey_club_owner):  
                    serializer = Jockey_club_owner1Serializer(transaction)
                    transaction_type = "Paid to"
                elif isinstance(transaction, Coins_trader_to_User):
                    serializer = User1Serializer(transaction)
                    transaction_type = "Paid to User"
                else: 
                    continue
                data = serializer.data
                dict = {"transaction_type": transaction_type}
                dict.update(data)
                transaction_data.append(dict)
            return Response({"Transactions_History": transaction_data})
        except Coins_trader.DoesNotExist:
            return Response({'error': 'Club owner not found.'})
        except Coins_club_owner_to_Coins_trader.DoesNotExist:
            return Response({'error': 'No transactions received from admin.'})
        except Coins_trader_to_Jockey_club_owner.DoesNotExist:
            return Response({'error': 'No transactions sent to trader.'})
        # except Exception as e:
        #     return Response({'error': 'Please provide a valid cointrader.'})
               
class UserTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            user_id = request.user.id   
            user = User.objects.get(uid=request.user.uid)
            received = Coins_trader_to_User.objects.filter(to_User=user)
            sent = User_to_Audio_Jockey.objects.filter(from_User=user)
            all_transactions = list(received) + list(sent)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            for transaction in all_transactions:
                if isinstance(transaction, Coins_trader_to_User):     
                    serializer = User1Serializer(transaction)
                    transaction_type = "Received from CoinTrader"
                elif isinstance(transaction, User_to_Audio_Jockey):  
                    serializer = Audio_Jockey1Serializer(transaction)
                    transaction_type = "Paid to"
                else: 
                    continue
                data = serializer.data
                dict = {"transaction_type": transaction_type}
                dict.update(data)
                transaction_data.append(dict)
            return Response({"Transactions_History": transaction_data})
        except User.DoesNotExist:
            return Response({'error': 'User not found.'})
        except Coins_trader_to_User.DoesNotExist:
            return Response({'error': 'No transactions received from cointrader.'})
        except User_to_Audio_Jockey.DoesNotExist:
            return Response({'error': 'No transactions sent to user.'})
        except Exception as e:
            return Response({'error': 'Please provide a valid User.'})
               

class Jockey_club_ownerTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            user_id = request.user.id   
            jockeyclubowner = Jockey_club_owner.objects.get(uid=request.user.uid)
            received = Coins_trader_to_Jockey_club_owner.objects.filter(to_Jockey_club_owner=jockeyclubowner)
            all_transactions = list(received)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            for transaction in all_transactions:
                if isinstance(transaction, Coins_trader_to_Jockey_club_owner):     
                    serializer = Jockey_club_owner1Serializer(transaction)
                    transaction_type = "Received from Cointrader"
                else: 
                    continue
                data = serializer.data
                dict = {"transaction_type": transaction_type}
                dict.update(data)
                transaction_data.append(dict)
            return Response({"Transactions_History": transaction_data})
        except Jockey_club_owner.DoesNotExist:
            return Response({'error': 'Jockey_club_owner not found.'})
        except Coins_trader_to_Jockey_club_owner.DoesNotExist:
            return Response({'error': 'No transactions received from CoinTrader.'})
        except Exception as e:
            return Response({'error': 'Please provide a valid Jockey_club_owner.'})
               

class Audio_JockeyTransactionHistoryView(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, id=None):
        try:
            user_id = request.user.id   
            audiojockey = Audio_Jockey.objects.get(uid=request.user.uid)
            received = User_to_Audio_Jockey.objects.filter(to_Audio_Jockey=audiojockey)
            all_transactions = list(received)
            all_transactions.sort(key=lambda x: x.created_date, reverse=True)
            transaction_data = []
            for transaction in all_transactions:
                if isinstance(transaction, User_to_Audio_Jockey):     
                    serializer = Audio_Jockey1Serializer(transaction)
                    transaction_type = "Received from User"
                else: 
                    continue
                data = serializer.data
                dict = {"transaction_type": transaction_type}
                dict.update(data)
                transaction_data.append(dict)
            return Response({"Transactions_History": transaction_data})
        except Audio_Jockey.DoesNotExist:
            return Response({'error': 'Audio_Jockey not found.'})
        except User_to_Audio_Jockey.DoesNotExist:
            return Response({'error': 'No transactions received from User.'})
        except Exception as e:
            return Response({'error': 'Please provide a valid Audio_Jockey.'})
               