from collections import defaultdict


from decimal import Decimal


from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from profil.models import Profil
from .models import Kirim, Chiqim, Valyuta, Kimdan, Uchun
from .forms import HisobFilterForm, ChiqimForm, KirimForm, ValyutaForm, UchunForm, KimdanForm, ValyutaKursForm


@login_required
def hisob(request):
    pr = Profil.objects.filter(user=request.user).first()
    if not pr.is_login:
        return redirect('profil:login')
    form = HisobFilterForm(request.GET)
    user = request.user
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    valuta = request.GET.get('valuta')
    summa_type = request.GET.get('summa_type')
    kimdan = request.GET.get('kimdan')
    uchun = request.GET.get('uchun')
    vals = Valyuta.objects.all()

    kirimlar = Kirim.objects.filter(user=user).order_by('-sana')
    chiqimlar = Chiqim.objects.filter(user=user).order_by('-sana')

    if start_date:
        kirimlar = kirimlar.filter(sana__gte=start_date)
        chiqimlar = chiqimlar.filter(sana__gte=start_date)

    if end_date:
        kirimlar = kirimlar.filter(sana__lte=end_date)
        chiqimlar = chiqimlar.filter(sana__lte=end_date)

    v = Valyuta.objects.filter(user=user)

    if not valuta:
        valuta = len(vals) - len(v)

    if v.exists():
        kirimlar = kirimlar.filter(valuta_id=valuta)
        chiqimlar = chiqimlar.filter(valuta_id=valuta)
        val = vals.filter(id=valuta).first()
    else:
        val = len(vals) - len(v)

    if summa_type:
        kirimlar = kirimlar.filter(summa_type=summa_type)
        chiqimlar = chiqimlar.filter(summa_type=summa_type)

    if kimdan:
        k = Kimdan.objects.filter(id=kimdan).first()
        kirimlar = kirimlar.filter(kimdan=k)
    if uchun:
        u = Uchun.objects.filter(id=uchun).first()
        chiqimlar = chiqimlar.filter(uchun=u)

    uchuns = Uchun.objects.filter(user=request.user)
    kimdans = Kimdan.objects.filter(user=request.user)

    jami_kirim = kirimlar.aggregate(Sum('summa'))['summa__sum'] or 0
    jami_chiqim = chiqimlar.aggregate(Sum('summa'))['summa__sum'] or 0
    balans = jami_kirim - jami_chiqim

    ctx = {
        'form': form,
        'kirimlar': kirimlar,
        'chiqimlar': chiqimlar,
        'jami_kirim': jami_kirim,
        'jami_chiqim': jami_chiqim,
        'balans': balans,
        'valuta': val,
        'valyutalar': v,
        'kimdans': kimdans,
        'uchuns': uchuns,
    }

    return render(request, 'transactions/hisob.html', ctx)





@login_required
def kirim_qosh(request):
    pr = Profil.objects.filter(user=request.user).first()
    if not pr.is_login:
        return redirect('profil:login')
    if request.method == 'POST':
        form = KirimForm(request.POST, user=request.user)
        if form.is_valid():
            kirim = form.save(commit=False)
            kirim.user = request.user
            kirim.save()
            return redirect('transactions:hisob')
    else:
        form = KirimForm(user=request.user)

    return render(request, 'transactions/kirim_qosh.html', {'form': form})


@login_required
def chiqim_qosh(request):
    pr = Profil.objects.filter(user=request.user).first()
    if not pr.is_login:
        return redirect('profil:login')
    if request.method == 'POST':
        form = ChiqimForm(request.POST, user=request.user)
        if form.is_valid():
            chiqim = form.save(commit=False)
            chiqim.user = request.user
            chiqim.save()

            return redirect('transactions:hisob')
    
    else:
        form = ChiqimForm(user=request.user)

    return render(request, 'transactions/chiqim_qosh.html', {'form': form})


@login_required
def valyuta_qosh(request):
    pr = Profil.objects.filter(user=request.user).first()
    if not pr.is_login:
        return redirect('profil:login')
    if request.method == 'POST':
        form = ValyutaForm(request.POST)
        if form.is_valid():
            valyuta = form.save(commit=False)
            valyuta.user = request.user
            valyuta.save()
            return redirect('transactions:hisob')
    else:
        form = ValyutaForm()

    return render(request, 'transactions/valyuta_qosh.html', {'form': form})



@login_required
def uchun_qosh(request):
    pr = Profil.objects.filter(user=request.user).first()
    if not pr.is_login:
        return redirect('profil:login')
    if request.method == 'POST':
        form = UchunForm(request.POST)
        if form.is_valid():
            uchun = form.save(commit=False)
            uchun.user = request.user
            uchun.save()
            return redirect('transactions:chiqim_qosh')
    else:
        form = UchunForm()

    return render(request, 'transactions/uchun_qosh.html', {'form': form})


@login_required
def kimdan_qosh(request):
    pr = Profil.objects.filter(user=request.user).first()
    if not pr.is_login:
        return redirect('profil:login')
    if request.method == 'POST':
        form = KimdanForm(request.POST)
        if form.is_valid():
            kimdan = form.save(commit=False)
            kimdan.user = request.user
            kimdan.save()
            return redirect('transactions:kirim_qosh')
    else:
        form = KimdanForm()

    return render(request, 'transactions/kimdan_qosh.html', {'form': form})



@login_required
def kurs_kirit(request):
    pr = Profil.objects.filter(user=request.user).first()
    if not pr.is_login:
        return redirect('profil:login')
    if request.method == 'POST':
        form = ValyutaKursForm(request.POST, user=request.user)
        if form.is_valid():
            asosiy = form.cleaned_data['asosiy_valyuta']
            kurslar = {}

            for key, value in form.cleaned_data.items():
                if key.startswith('kurs_') and value:
                    val_id = int(key.replace('kurs_', ''))
                    kurslar[val_id] = Decimal(value)

            valyutalar = Valyuta.objects.filter(id__in=kurslar.keys(), user=request.user)

            kirimlar = Kirim.objects.filter(user=request.user)
            chiqimlar = Chiqim.objects.filter(user=request.user)

            jami_kirim = Decimal(0)
            jami_chiqim = Decimal(0)

            valyuta_statistikasi = defaultdict(lambda: {
                'kirim': Decimal(0),
                'chiqim': Decimal(0),
                'kirim_asosiy': Decimal(0),
                'chiqim_asosiy': Decimal(0),
            })

            for kirim in kirimlar:
                kurs = kurslar.get(kirim.valuta.id, Decimal(1))
                valyuta_statistikasi[kirim.valuta.id]['kirim'] += kirim.summa
                valyuta_statistikasi[kirim.valuta.id]['kirim_asosiy'] += kirim.summa * kurs
                jami_kirim += kirim.summa * kurs

            for chiqim in chiqimlar:
                kurs = kurslar.get(chiqim.valuta.id, Decimal(1))
                valyuta_statistikasi[chiqim.valuta.id]['chiqim'] += chiqim.summa
                valyuta_statistikasi[chiqim.valuta.id]['chiqim_asosiy'] += chiqim.summa * kurs
                jami_chiqim += chiqim.summa * kurs

            balans = jami_kirim - jami_chiqim

            kurslar_qiymatlari = []
            for val in valyutalar:
                statistik = valyuta_statistikasi[val.id]
                kurs_qiymati = kurslar.get(val.id, Decimal(1))
                kurslar_qiymatlari.append({
                    'valyuta': val,
                    'kurs': kurs_qiymati,
                    'kirim': round(statistik['kirim'], 2),
                    'chiqim': round(statistik['chiqim'], 2),
                    'kirim_asosiy': round(statistik['kirim_asosiy'], 2),
                    'chiqim_asosiy': round(statistik['chiqim_asosiy'], 2),
                })

            return render(request, 'transactions/kurs_natija.html', {
                'asosiy': asosiy,
                'kurslar_qiymatlari': kurslar_qiymatlari,
                'jami_kirim': round(jami_kirim, 2),
                'jami_chiqim': round(jami_chiqim, 2),
                'balans': round(balans, 2),
            })

    else:
        form = ValyutaKursForm(user=request.user)

    return render(request, 'transactions/kurs_kirit.html', {'form': form})


@login_required
def kirim(request):
    pr = Profil.objects.filter(user=request.user).first()
    if not pr.is_login:
        return redirect('profil:login')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    valuta = request.GET.get('valuta')
    summa_type = request.GET.get('summa_type')
    kimdan = request.GET.get('kimdan')

    kirimlar = Kirim.objects.filter(user=request.user).order_by('-sana')

    if start_date:
        kirimlar = kirimlar.filter(sana__gte=start_date)
    if end_date:
        kirimlar = kirimlar.filter(sana__lte=end_date)
    if valuta:
        vs = Valyuta.objects.filter(id=valuta).first()
        kirimlar = kirimlar.filter(valuta=vs)
    if summa_type:
        kirimlar = kirimlar.filter(summa_type=summa_type)
    if kimdan:
        kirimlar = kirimlar.filter(kimdan_id=kimdan)

    kimdan_choices = Kimdan.objects.filter(user=request.user)

    if valuta:
        jami_kirim = sum(k.summa for k in kirimlar) if kirimlar.exists() else 0
    else:
        jami_kirim = "--"

    val_k = Valyuta.objects.filter(user=request.user)
    dic, a = {}, Kirim.objects.filter(user=request.user)
    if start_date:
        a = a.filter(sana__gte=start_date)
    if end_date:
        a = a.filter(sana__lte=end_date)
    for i in val_k:
        kv = sum(k.summa for k in a.filter(valuta=i))
        if i not in dic.keys():
            dic[i.short] = kv
        else:
            dic[i.short] += kv

    context = {
        'kirimlar': kirimlar,
        'jami_kirim': jami_kirim,
        'valyutalar': Valyuta.objects.filter(user=request.user) or [],
        'kimdan_choices': kimdan_choices,
        'valuta': Valyuta.objects.get(id=valuta) if valuta else None,
        'dic': dic,
        'form': request.GET,
    }
    return render(request, 'transactions/kirim.html', context)


@login_required
def chiqim(request):
    pr = Profil.objects.filter(user=request.user).first()
    if not pr.is_login:
        return redirect('profil:login')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    valuta_id = request.GET.get('valuta')
    summa_type = request.GET.get('summa_type')
    uchun = request.GET.get('uchun')

    chiqimlar = Chiqim.objects.filter(user=request.user).order_by('-sana')



    if start_date:
        chiqimlar = chiqimlar.filter(sana__gte=start_date)
    if end_date:
        chiqimlar = chiqimlar.filter(sana__lte=end_date)
    if valuta_id:
        chiqimlar = chiqimlar.filter(valuta_id=valuta_id)
    if summa_type:
        chiqimlar = chiqimlar.filter(summa_type=summa_type)
    if uchun:
        chiqimlar = chiqimlar.filter(uchun_id=uchun)

    uchun_choices = Uchun.objects.filter(user=request.user)

    if valuta_id:
        jami_chiqim = sum(k.summa for k in chiqimlar) if chiqimlar.exists() else 0
    else:
        jami_chiqim = "--"

    val_k = Valyuta.objects.filter(user=request.user)
    dic, a = {}, Chiqim.objects.filter(user=request.user)
    if start_date:
        a = a.filter(sana__gte=start_date)
    if end_date:
        a = a.filter(sana__lte=end_date)
    for i in val_k:
        kv = sum(k.summa for k in a.filter(valuta=i))
        if i not in dic.keys():
            dic[i.short] = kv
        else:
            dic[i.short] += kv

    context = {
        'chiqimlar': chiqimlar,
        'jami_chiqim': jami_chiqim,
        'valyutalar': Valyuta.objects.filter(user=request.user) or [],
        'uchun_choices': uchun_choices,
        'dic': dic,
        'valuta': Valyuta.objects.get(id=valuta_id) if valuta_id else None,
        'form': request.GET,
    }
    return render(request, 'transactions/chiqim.html', context)

