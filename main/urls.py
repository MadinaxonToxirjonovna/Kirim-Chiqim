from django.urls import path
from .views import index_view, contact

app_name = 'main'

urlpatterns = [
    path('', index_view, name='index'),
    path('contact/', contact, name='contact'),

]
