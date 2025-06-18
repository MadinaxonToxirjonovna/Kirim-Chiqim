from django.db import models
from django.contrib.auth.models import User


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rasm = models.ImageField(upload_to='profil_rasmlari/', default='profile/default.png', blank=True, null=True)
    manzil = models.CharField(max_length=255, blank=True, null=True)
    tugilgan_sana = models.DateField(blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
    tasdiqla_kod = models.CharField(max_length=6, blank=True, null=True)
    currency = models.ForeignKey('transactions.Valyuta', on_delete=models.SET_NULL, null=True, blank=True)
    kod_vaqt = models.DateTimeField(auto_now=True)
    is_login = models.BooleanField(default=False)
    is_profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} profili"
