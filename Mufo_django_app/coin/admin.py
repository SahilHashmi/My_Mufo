from django.contrib import admin
from .models import*

admin.site.register(Admin_to_Coins_club_owner)
admin.site.register(Coins_club_owner_to_Coins_trader)
admin.site.register(Coins_trader_to_Jockey_club_owner)
admin.site.register(Coins_trader_to_User)
admin.site.register(User_to_Audio_Jockey)

