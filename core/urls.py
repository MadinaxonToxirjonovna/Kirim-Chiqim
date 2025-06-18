from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path('update/', ProfilListCreateAPIView.as_view()),
    path('profil/<int:pk>/', ProfilRetrieveUpdateDestroyAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('login/', obtain_auth_token),
    path('logout/', LogoutAPIView.as_view()),
    path('uchun/', UchunListCreateAPIView.as_view()),
    path('uchun/<int:pk>/', UchunDetailAPIView.as_view()),
    path('kimdan/', KimdanListCreateAPIView.as_view()),
    path('kimdan/<int:pk>/', KimdanDetailAPIView.as_view()),
    path('valyuta/', ValyutaListCreateAPIView.as_view()),
    path('valyuta/<int:pk>/', ValyutaDetailAPIView.as_view()),
    path('kirim/', KirimListCreateAPIView.as_view()),
    path('kirim/<int:pk>/', KirimDetailAPIView.as_view()),
    path('chiqim/', ChiqimListCreateAPIView.as_view()),
    path('chiqim/<int:pk>/', ChiqimDetailAPIView.as_view()),

]
