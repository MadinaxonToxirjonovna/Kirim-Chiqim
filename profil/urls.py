from django.urls import path
from .views import *

app_name = 'profil'

urlpatterns = [
    path('profil/', profil, name='profil'),
    path('tahrirlash/', tahrirlash, name='tahrirlash'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('verify/', verify_view, name='verify'),
    path('logout/', logout_view, name='logout'),
]
