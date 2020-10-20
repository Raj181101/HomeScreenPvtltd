from django.contrib import admin
from django.urls import path
from customer_store import views as views

urlpatterns = [
    
    path('your-location',views.user_location,name='user_location'),

]
