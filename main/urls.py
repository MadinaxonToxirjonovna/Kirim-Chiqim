from django.urls import path
from . import views

app_name = 'main'  

urlpatterns = [
    path('', views.index_view, name='index'),         
    path('contact/', views.contact, name='contact'), 
]
