from django.contrib import admin

from profil.models import Profil
# Register your models here.

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefon', 'manzil', 'tugilgan_sana', 'kod_vaqt')
    search_fields = ('user__username', 'telefon', 'manzil')

