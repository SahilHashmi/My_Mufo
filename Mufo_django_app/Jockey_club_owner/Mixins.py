# from django.conf import settings
# from twilio.rest import Client 
# from Mufo import settings

# def send_otp_on_phone(phone_number, otp):
#     account_sid = settings.account_sid
#     auth_token = settings.auth_token
#     twilio_phone_number = settings.twilio_phone_number
#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         body=f"Your OTP is: {otp}",
#         from_=twilio_phone_number,
#         to=phone_number
#     )

#     return message.sid
import requests

def send_otp_on_phone(mobile_number, otp):
    API_KEY = '397239AMFkn6shwxk64787c77P1'
    SENDER_ID = '998765'
    # ROUTE = '4'  # Route for transactional SMS

    url = "https://control.msg91.com/api/v5/otp"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "authkey": API_KEY,
        "template_id": "64787cd3d6fc050aa44d0932",  # The ID of the template you have created in Msg91
        "mobile": mobile_number,
        "otp": otp,
        "sender": SENDER_ID,
        # "route": ROUTE
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        # OTP sent successfully
        return True
    else:
        # Failed to send OTP
        return False