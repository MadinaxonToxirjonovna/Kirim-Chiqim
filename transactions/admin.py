from django.contrib import admin
from .models import Valyuta, Kirim, Chiqim


class ValyutaAdmin(admin.ModelAdmin):
    list_display = ('name', 'short', 'user')
    search_fields = ('name', 'short')
    list_filter = ('user',)


class KirimAdmin(admin.ModelAdmin):
    list_display = ('kimdan', 'summa', 'summa_type', 'valuta', 'sana', 'user')
    search_fields = ('kimdan', 'valuta__name')
    list_filter = ('summa_type', 'valuta', 'user')
    list_editable = ('summa_type', 'valuta')


class ChiqimAdmin(admin.ModelAdmin):
    list_display = ('uchun', 'summa', 'summa_type', 'valuta', 'sana', 'user')
    search_fields = ('uchun', 'valuta__name')
    list_filter = ('summa_type', 'valuta', 'user')
    list_editable = ('summa_type', 'valuta')


admin.site.register(Valyuta, ValyutaAdmin)
admin.site.register(Kirim, KirimAdmin)
admin.site.register(Chiqim, ChiqimAdmin)
