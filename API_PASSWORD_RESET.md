# API REST pour la réinitialisation de mot de passe

## Installation des dépendances

```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
```

## Configuration dans settings.py

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # En haut
    # ...
]

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React
    "http://localhost:8080",  # Vue
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## Créer l'API (UserApp/api_views.py)

```python
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .models import Utilisateur
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


@api_view(['POST'])
@permission_classes([AllowAny])
def api_password_reset_request(request):
    """
    API endpoint pour demander une réinitialisation de mot de passe
    
    POST /api/user/password-reset/
    {
        "email": "user@example.com"
    }
    """
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'Email is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = Utilisateur.objects.get(email=email)
        
        # Générer token et uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Construire le lien de réinitialisation
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        
        # Envoyer l'email
        send_mail(
            subject="Réinitialisation de mot de passe - SmartLibrary",
            message=f"""
            Bonjour {user.first_name},
            
            Vous avez demandé la réinitialisation de votre mot de passe.
            
            Cliquez sur le lien ci-dessous pour créer un nouveau mot de passe :
            {reset_url}
            
            Ce lien est valide pendant 24 heures.
            
            Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.
            
            Cordialement,
            L'équipe SmartLibrary
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        
        return Response({
            'message': 'Password reset email sent successfully',
            'email': email
        }, status=status.HTTP_200_OK)
        
    except Utilisateur.DoesNotExist:
        # Ne pas révéler si l'email existe ou non (sécurité)
        return Response({
            'message': 'If the email exists, a reset link will be sent'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_password_reset_confirm(request):
    """
    API endpoint pour confirmer la réinitialisation
    
    POST /api/user/password-reset-confirm/
    {
        "uid": "MQ",
        "token": "abc123-...",
        "new_password": "NewSecurePass123!"
    }
    """
    uid = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')
    
    if not all([uid, token, new_password]):
        return Response(
            {'error': 'uid, token, and new_password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Décoder l'uid
        user_id = force_str(urlsafe_base64_decode(uid))
        user = Utilisateur.objects.get(pk=user_id)
        
        # Vérifier le token
        if not default_token_generator.check_token(user, token):
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valider le nouveau mot de passe
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response(
                {'error': list(e.messages)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Changer le mot de passe
        user.set_password(new_password)
        user.save()
        
        return Response({
            'message': 'Password has been reset successfully'
        }, status=status.HTTP_200_OK)
        
    except (TypeError, ValueError, OverflowError, Utilisateur.DoesNotExist):
        return Response(
            {'error': 'Invalid reset link'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def api_verify_reset_token(request):
    """
    Vérifier si un token de réinitialisation est valide
    
    POST /api/user/verify-reset-token/
    {
        "uid": "MQ",
        "token": "abc123-..."
    }
    """
    uid = request.data.get('uid')
    token = request.data.get('token')
    
    if not all([uid, token]):
        return Response(
            {'error': 'uid and token are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = Utilisateur.objects.get(pk=user_id)
        
        if default_token_generator.check_token(user, token):
            return Response({
                'valid': True,
                'message': 'Token is valid'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'valid': False,
                'error': 'Token is invalid or expired'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except (TypeError, ValueError, OverflowError, Utilisateur.DoesNotExist):
        return Response({
            'valid': False,
            'error': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)
```

## URLs API (UserApp/api_urls.py)

```python
from django.urls import path
from .api_views import (
    api_password_reset_request,
    api_password_reset_confirm,
    api_verify_reset_token
)

urlpatterns = [
    path('password-reset/', api_password_reset_request, name='api_password_reset'),
    path('password-reset-confirm/', api_password_reset_confirm, name='api_password_reset_confirm'),
    path('verify-reset-token/', api_verify_reset_token, name='api_verify_reset_token'),
]
```

## Inclure dans SmartLibrary/urls.py

```python
urlpatterns = [
    # ...
    path('api/user/', include('UserApp.api_urls')),
]
```

## Ajouter FRONTEND_URL dans settings.py

```python
# URL du frontend (React, Vue, Angular, etc.)
FRONTEND_URL = 'http://localhost:3000'  # Développement
# FRONTEND_URL = 'https://smartlibrary.com'  # Production
```

---

## Frontend React Example

### 1. Demander réinitialisation

```javascript
// src/components/ForgotPassword.jsx
import { useState } from 'react';
import axios from 'axios';

function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post(
        'http://localhost:8000/api/user/password-reset/',
        { email }
      );
      setMessage(response.data.message);
    } catch (error) {
      setMessage('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="forgot-password">
      <h2>Forgot Password</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Sending...' : 'Send Reset Link'}
        </button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default ForgotPassword;
```

### 2. Réinitialiser le mot de passe

```javascript
// src/components/ResetPassword.jsx
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

function ResetPassword() {
  const { uid, token } = useParams();
  const navigate = useNavigate();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [validToken, setValidToken] = useState(false);

  useEffect(() => {
    // Vérifier le token au chargement
    axios.post('http://localhost:8000/api/user/verify-reset-token/', {
      uid,
      token
    })
    .then(() => setValidToken(true))
    .catch(() => setError('Invalid or expired reset link'));
  }, [uid, token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    setLoading(true);
    
    try {
      await axios.post(
        'http://localhost:8000/api/user/password-reset-confirm/',
        {
          uid,
          token,
          new_password: password
        }
      );
      alert('Password reset successful!');
      navigate('/login');
    } catch (error) {
      setError(error.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (!validToken && !error) return <div>Verifying...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="reset-password">
      <h2>Reset Your Password</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          placeholder="New Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Resetting...' : 'Reset Password'}
        </button>
      </form>
    </div>
  );
}

export default ResetPassword;
```

### 3. Routes React

```javascript
// src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:uid/:token" element={<ResetPassword />} />
        {/* ... autres routes */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

---

## Test avec Postman/Thunder Client

### 1. Demander réinitialisation

```
POST http://localhost:8000/api/user/password-reset/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

### 2. Vérifier token

```
POST http://localhost:8000/api/user/verify-reset-token/
Content-Type: application/json

{
  "uid": "MQ",
  "token": "abc123-token-from-email"
}
```

### 3. Réinitialiser mot de passe

```
POST http://localhost:8000/api/user/password-reset-confirm/
Content-Type: application/json

{
  "uid": "MQ",
  "token": "abc123-token-from-email",
  "new_password": "NewSecurePassword123!"
}
```

---

## Sécurité API

### Rate Limiting

```python
from rest_framework.throttling import AnonRateThrottle

class PasswordResetThrottle(AnonRateThrottle):
    rate = '5/hour'

# Dans les vues
@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([PasswordResetThrottle])
def api_password_reset_request(request):
    # ...
```

### CORS en production

```python
# Production
CORS_ALLOWED_ORIGINS = [
    "https://smartlibrary.com",
    "https://www.smartlibrary.com",
]

CORS_ALLOW_CREDENTIALS = True
```

---

## Avantages de l'approche API

✅ Découplage frontend/backend  
✅ Support multi-plateformes (web, mobile)  
✅ Meilleure scalabilité  
✅ Architecture moderne (SPA)  
✅ Testabilité améliorée  

---

## Documentation complète

Pour plus d'informations, consultez `GMAIL_SETUP.md`
