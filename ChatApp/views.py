from django.shortcuts import render

# ChatApp/views.py
from django.views.generic import TemplateView

class ChatbotView(TemplateView):
    """
    Displays the chat interface page.
    """
    template_name = 'chat/chat.html'
