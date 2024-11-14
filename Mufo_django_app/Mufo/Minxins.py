
from . import settings 
from django.http import HttpResponse,JsonResponse

import requests

def send_otp_on_phone(mobile_number, otp):
    API_KEY = settings.API_KEY
    SENDER_ID = settings.SENDER_ID
    ROUTE = settings.ROUTE
    Templte_id =  settings.Templte_id

    url = "https://control.msg91.com/api/v5/otp"
    headers = {
        "Content-Type": "application/json",
        "authkey": API_KEY
    }
    payload = {
        "template_id": Templte_id ,  
        "mobile": mobile_number,
        "OTP": otp,
        "sender": SENDER_ID,
        "route": ROUTE
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response)
    if response.status_code == 200:
        # OTP sent successfully
        return True
    else:
        # Failed to send OTP
        return False
    
from User.models import User 
from Audio_Jockey.models import Audio_Jockey
from Coins_club_owner.models import Coins_club_owner
from Coins_trader.models import Coins_trader
from Jockey_club_owner.models import Jockey_club_owner
from master.models import *
def authenticate_token(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]

        models = [Common,User, Audio_Jockey,Jockey_club_owner, Coins_club_owner,Coins_trader,]
        user = None

        for model in models:
            try:
                user = model.objects.get(token=token)
                break
            except model.DoesNotExist:
                continue

        if user is None:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        request.user = user
        return view_func(request, *args, **kwargs)

    return wrapper

