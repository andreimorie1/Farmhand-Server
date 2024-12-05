from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_farmer, name='register_farmer'),
    path('login/', views.login_farmer, name='login_farmer'),
    path('update/', views.update_farmer, name='update_farmer'),
    path('delete/', views.delete_farmer, name='delete_farmer'),
    path('get_farmer/', views.get_farmer, name='get_farmer'),

]