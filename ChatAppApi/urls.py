# ChatAppApi/urls.py
from django.urls import path
from .views import chatbot_api

urlpatterns = [
    path('', chatbot_api, name='chat_api'),   # /api/chat/
]
