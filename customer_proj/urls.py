from django.contrib import admin
from django.urls import path
from customer_store import views as views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('api/customer/<int:id>/', views.customer, name='customer'),
    path('api/customers/', views.all_customer, name='all_customer'),
    path('api/browse/', views.api_browse, name='api_browse'),
    path('api/create/', views.bookmark_create, name='bookmark_create'),

]
