from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('library/', include('LivreApp.urls')),  # correction : éviter conflit avec ''
    path('api/', include('LivreAppApi.urls')),
    path('books/', views.all_books, name='all_books'),
    path('avis/', include('AvisApp.urls')),
    path('api/avis/', include('AvisAppApi.urls')),
    path('Panier/', include('PanierApp.urls')),
    path('api/', include('PanierAppApi.urls')),
    path('profile/', include('ProfileApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user/', include('UserApp.urls')),
    path('chat/', include('ChatApp.urls')),
    path('api/chat/', include('ChatAppApi.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
