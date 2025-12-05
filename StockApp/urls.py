from django.urls import path, include
from django.contrib import admin
from StockApp import views
app_name = "StockApp" 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stats/', views.stock_stats_view, name='stock_stats'),
    path("stats/data/", views.stock_stats_data, name="stock_stats_data"),
]
