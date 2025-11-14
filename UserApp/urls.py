from django.urls import path
from .views import register, CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),  # Register page
    path('login/', CustomLoginView.as_view(template_name='UserApp/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
