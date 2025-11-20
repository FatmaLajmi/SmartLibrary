from django.urls import path
from .views import register, CustomLoginView, logout_view

urlpatterns = [
    path('register/', register, name='register'),  # Register page
    path('login/', CustomLoginView.as_view(template_name='UserApp/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
]
