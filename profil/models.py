from django.db import models
from django.contrib.auth.models import User


class Profil(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rasm = models.ImageField(upload_to='media/', default='media/default.png', blank=True, null=True)
    manzil = models.CharField(max_length=255, blank=True, null=True)
    tugilgan_sana = models.DateField(blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
    tasdiqla_kod = models.CharField(blank=True, null=True)
    is_login = models.BooleanField(default=False)
    kod_vaqt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
