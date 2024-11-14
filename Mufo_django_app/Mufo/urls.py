"""Mufo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "Mufo Admin Portal"
admin.site.site_title = "Mufo Admin Portal"
admin.site.index_title = "Welcome to Mufo admin Portal"



urlpatterns = [
    path('admin/', admin.site.urls),
    path("audio_jockey/", include("Audio_Jockey.urls")),
    path("Coins_club_owner/", include("Coins_club_owner.urls")),
    path("coins_trader/", include("Coins_trader.urls")),
    path("Jockey_club_owner/", include("Jockey_club_owner.urls")),
    path("User/", include("User.urls")),
    path('api/chat/', include('Chat.api_urls')),
    path('chat/', include('Chat.urls'), name='chat'),
    path('coins/', include('coin.urls'), name='coin'),
    path('master/', include('master.urls'), name='master'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
