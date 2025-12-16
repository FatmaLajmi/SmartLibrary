"""
Custom views for password reset functionality with additional security and validation
"""
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import logging

logger = logging.getLogger(__name__)


class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view with logging and rate limiting support
    """
    template_name = 'UserApp/password_reset.html'
    email_template_name = 'UserApp/password_reset_email.html'
    subject_template_name = 'UserApp/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        """Log password reset requests"""
        email = form.cleaned_data['email']
        logger.info(f"Password reset requested for email: {email}")
        messages.success(
            self.request, 
            "If this email address exists in our system, you will receive a password reset email."
        )
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Log failed attempts"""
        logger.warning(f"Invalid password reset form submission from IP: {self.get_client_ip()}")
        return super().form_invalid(form)
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom password reset confirm view with additional validation
    """
    template_name = 'UserApp/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    
    def form_valid(self, form):
        """Validate new password and log successful reset"""
        user = form.save()
        logger.info(f"Password successfully reset for user: {user.email}")
        messages.success(self.request, "Your password has been reset successfully!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Log validation errors"""
        logger.warning(f"Password reset validation failed for token")
        messages.error(self.request, "The password does not meet the security requirements.")
        return super().form_invalid(form)
