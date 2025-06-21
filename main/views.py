
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from datetime import date, timedelta, datetime
from transactions.models import Kirim, Chiqim, Valyuta
from django.db.models import Sum
from profil.models import Profil


@login_required
def index_view(request):
    pr = Profil.objects.filter(user=request.user).first()
    if (not pr.is_login) and (not request.user.is_authenticated):
        return redirect('profil:login')

    today = datetime.today()
    haftalik_hisobot = []
    for i in range(7):
        sana = today - timedelta(days=i)
        kirim = Kirim.objects.filter(user=request.user, sana=sana).aggregate(Sum('summa'))['summa__sum'] or 0
        chiqim = Chiqim.objects.filter(user=request.user, sana=sana).aggregate(Sum('summa'))['summa__sum'] or 0
        haftalik_hisobot.append({'sana': sana.strftime('%d-%m-%Y'), 'kirim': kirim, 'chiqim': chiqim})
    haftalik_hisobot = sorted(haftalik_hisobot, key=lambda x: x['sana'], reverse=True)
    oylik_data = []
    for i in range(30):
        sana = today - timedelta(days=i)
        kirim = Kirim.objects.filter(user=request.user, sana=sana).aggregate(Sum('summa'))['summa__sum'] or 0
        chiqim = Chiqim.objects.filter(user=request.user, sana=sana).aggregate(Sum('summa'))['summa__sum'] or 0
        oylik_data.append({'sana': sana.strftime('%Y-%m-%d'), 'kirim': kirim, 'chiqim': chiqim})

    oylik_data = sorted(oylik_data, key=lambda x: x['sana'], reverse=True)
    oylik_paginator = Paginator(oylik_data, 10)
    oylik_page = request.GET.get('oylik_page')
    oylik = oylik_paginator.get_page(oylik_page)


    yillik_data = []
    for year in range(today.year - 5, today.year + 1):
        kirim = Kirim.objects.filter(user=request.user, sana__year=year).aggregate(Sum('summa'))['summa__sum'] or 0
        chiqim = Chiqim.objects.filter(user=request.user, sana__year=year).aggregate(Sum('summa'))['summa__sum'] or 0
        yillik_data.append({'sana': str(year), 'kirim': kirim, 'chiqim': chiqim})
    yillik_data = sorted(yillik_data, key=lambda x: x['sana'], reverse=True)
    yillik_paginator = Paginator(yillik_data, 10)
    yillik_page = request.GET.get('yillik_page')
    yillik = yillik_paginator.get_page(yillik_page)

    yil_sum = Kirim.objects.filter(user=request.user, sana__year=today.year).aggregate(Sum('summa'))['summa__sum'] or 0

    valuta_id = request.GET.get('valuta')
    valuta = Valyuta.objects.get(id=valuta_id) if valuta_id else None

    context = {
        'haftalik_hisobot': haftalik_hisobot,
        'oylik': oylik,
        'yillik': yillik,
        'yil_sum': yil_sum,
        'valuta': valuta,
    }

    return render(request, 'index.html', context)


def contact(request):
    return render(request, 'contact.html')
