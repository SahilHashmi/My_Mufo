# from django.conf import settings
from twilio.rest import Client 
from Mufo import settings

def send_otp_on_phone(phone_number, otp):
    account_sid = settings.account_sid
    auth_token = settings.auth_token
    twilio_phone_number = settings.twilio_phone_number
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your OTP is: {otp}",
        from_=twilio_phone_number,
        to=phone_number
    )

    return message.sid
