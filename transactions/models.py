from django.db import models
from django.contrib.auth.models import User


class Uchun(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nomi = models.CharField(max_length=100)

    def __str__(self):
        return self.nomi


class Kimdan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nomi = models.CharField(max_length=255)

    def __str__(self):
        return self.nomi


class Valyuta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10, blank=True, null=True)
    short = models.CharField(max_length=3)

    def __str__(self):
        return self.short


class Kirim(models.Model):
    summa_turi = (('naqd', 'Naqd'), ('plastik', 'Plastik'), ('bank', 'Bank'),)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kimdan = models.ForeignKey(Kimdan, on_delete=models.CASCADE)
    sana = models.DateField()
    summa = models.DecimalField(max_digits=12, decimal_places=2)
    summa_type = models.CharField(max_length=20, choices=summa_turi, default='naqd')
    valuta = models.ForeignKey(Valyuta, on_delete=models.CASCADE)
    izoh = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Kirim: {self.summa} so'm - {self.sana}"


class Chiqim(models.Model):
    summa_turi = (('naqd', 'Naqd'), ('plastik', 'Plastik'), ('bank', 'Bank'),)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uchun = models.ForeignKey(Uchun, on_delete=models.CASCADE)
    sana = models.DateField()
    summa = models.DecimalField(max_digits=12, decimal_places=2)
    summa_type = models.CharField(max_length=20, choices=summa_turi, default='naqd')
    valuta = models.ForeignKey(Valyuta, on_delete=models.CASCADE)
    izoh = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Chiqim: {self.summa} so'm - {self.sana}"
