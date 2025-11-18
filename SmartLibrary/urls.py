from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/', include('LivreAppApi.urls')),  # ton API
    path('avis/', include('AvisApp.urls')),         # frontend MVT
    path('api/avis/', include('AvisAppApi.urls')),
    path('Panier/', include('PanierApp.urls')),
    path('api/', include('PanierAppApi.urls')),
    path('profile/', include('ProfileApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user/', include('UserApp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
