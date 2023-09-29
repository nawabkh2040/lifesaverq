from django.contrib import admin
from django.urls import path 
from emergencyapp import views

urlpatterns = [
    path('',views.profile,name="profile"),
    path('display_qr_code/', views.display_qr_code, name='display_qr_code'),
]
