from django.urls import path
from .views import *

app_name = 'transactions'
urlpatterns = [
    path('hisob/', hisob, name='hisob'),
    path('kirim_qosh/', kirim_qosh, name='kirim_qosh'),
    path('chiqim_qosh/', chiqim_qosh, name='chiqim_qosh'),
    path('valyuta_qosh/', valyuta_qosh, name='valyuta_qosh'),
    path('uchun_qosh/', uchun_qosh, name='uchun_qosh'),
    path('kimdan_qosh/', kimdan_qosh, name='kimdan_qosh'),
    path('kurs_kirit/', kurs_kirit, name='kurs_kirit'),
    path('kirim/', kirim, name='kirim'),
    path('chiqim/', chiqim, name='chiqim'),

]
