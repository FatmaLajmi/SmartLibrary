# Configuration Gmail pour la réinitialisation de mot de passe - SmartLibrary

## 📧 Configuration Gmail/Google Workspace

### Étape 1 : Activer l'authentification à deux facteurs (2FA)

1. Allez sur votre compte Google : https://myaccount.google.com/
2. Cliquez sur **Sécurité** dans le menu de gauche
3. Dans la section "Connexion à Google", activez la **Validation en deux étapes**
4. Suivez les instructions pour configurer 2FA

### Étape 2 : Créer un mot de passe d'application

1. Une fois 2FA activé, retournez dans **Sécurité**
2. Recherchez "Mots de passe des applications" (ou allez directement sur : https://myaccount.google.com/apppasswords)
3. Sélectionnez "Application" → **Autre (nom personnalisé)**
4. Entrez "SmartLibrary Django" comme nom
5. Cliquez sur **Générer**
6. **Copiez le mot de passe de 16 caractères** (il sera affiché une seule fois)

### Étape 3 : Configurer Django settings.py

Dans `SmartLibrary/settings.py`, décommentez et configurez les lignes suivantes :

```python
# ----------------------------
#   EMAIL CONFIGURATION (PRODUCTION)
# ----------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre-email@gmail.com'  # Remplacez par votre Gmail
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'  # Mot de passe d'application (16 caractères)
DEFAULT_FROM_EMAIL = 'SmartLibrary <votre-email@gmail.com>'
SERVER_EMAIL = 'votre-email@gmail.com'

# Timeout pour réinitialisation (24 heures)
PASSWORD_RESET_TIMEOUT = 86400
```

### Étape 4 : Utiliser les variables d'environnement (RECOMMANDÉ)

**Ne jamais mettre vos credentials en dur dans le code !**

#### Créer un fichier `.env` à la racine du projet :

```env
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
```

#### Installer python-decouple :

```bash
pip install python-decouple
```

#### Modifier `settings.py` :

```python
from decouple import config

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = f'SmartLibrary <{config("EMAIL_HOST_USER")}>'
SERVER_EMAIL = config('EMAIL_HOST_USER')
```

#### Ajouter `.env` au `.gitignore` :

Le fichier `.env` est déjà dans votre `.gitignore`, donc vos credentials seront protégés.

---

## 🧪 Tester l'envoi d'email

### Mode développement (Console Backend) :

Par défaut, Django affiche les emails dans la console :

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Lancez le serveur :
```bash
python manage.py runserver
```

Allez sur : http://127.0.0.1:8000/user/password-reset/
L'email s'affichera dans la console/terminal.

### Mode production (Gmail SMTP) :

1. Configurez Gmail comme expliqué ci-dessus
2. Modifiez `EMAIL_BACKEND` dans settings.py
3. Testez l'envoi :

```python
# Dans le shell Django
python manage.py shell

from django.core.mail import send_mail

send_mail(
    'Test SmartLibrary',
    'Ceci est un test d\'envoi d\'email.',
    'votre-email@gmail.com',
    ['destinataire@example.com'],
    fail_silently=False,
)
```

---

## 🔐 Sécurité et bonnes pratiques

### 1. Rate Limiting (Protection contre les abus)

Installez Django Ratelimit :
```bash
pip install django-ratelimit
```

Ajoutez dans `UserApp/urls.py` :
```python
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

# Dans les vues personnalisées
@method_decorator(ratelimit(key='ip', rate='5/h', method='POST'), name='dispatch')
class CustomPasswordResetView(PasswordResetView):
    # ...
```

### 2. HTTPS en production

**Obligatoire pour la sécurité !**

Dans `settings.py` (production uniquement) :
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 3. Logging

Les tentatives de réinitialisation sont déjà loggées dans `password_reset_views.py`.

Configuration logging dans `settings.py` :
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'password_reset.log',
        },
    },
    'loggers': {
        'UserApp': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

Créez le dossier `logs/` :
```bash
mkdir logs
```

---

## 🚀 URLs de test

- Demander réinitialisation : http://127.0.0.1:8000/user/password-reset/
- Confirmation d'envoi : http://127.0.0.1:8000/user/password-reset/done/
- Login : http://127.0.0.1:8000/user/login/

---

## 📋 Checklist finale

- [ ] 2FA activé sur Gmail
- [ ] Mot de passe d'application créé
- [ ] `.env` créé avec credentials
- [ ] `python-decouple` installé
- [ ] `.env` dans `.gitignore`
- [ ] EMAIL_BACKEND configuré dans settings.py
- [ ] Test d'envoi d'email réussi
- [ ] Lien "Forgot password" ajouté à la page login
- [ ] Templates personnalisés créés
- [ ] HTTPS configuré (en production)
- [ ] Rate limiting activé (recommandé)
- [ ] Logging configuré

---

## 🆘 Troubleshooting

### Erreur : "SMTPAuthenticationError"
- Vérifiez que 2FA est activé
- Vérifiez le mot de passe d'application (16 caractères, sans espaces)
- Vérifiez EMAIL_HOST_USER et EMAIL_HOST_PASSWORD

### Erreur : "Connection refused"
- Vérifiez EMAIL_PORT (587 pour TLS)
- Vérifiez votre firewall
- Vérifiez que EMAIL_USE_TLS = True

### Email non reçu
- Vérifiez les spams
- Vérifiez les logs Django
- Testez avec send_mail() dans le shell
- Vérifiez que l'email existe dans la base de données

### Lien expiré
- Par défaut : 24h (PASSWORD_RESET_TIMEOUT = 86400)
- Augmentez la valeur si nécessaire

---

## 📞 Support

Pour plus d'aide :
- Documentation Django : https://docs.djangoproject.com/en/5.0/topics/email/
- Gmail SMTP : https://support.google.com/mail/answer/7126229
