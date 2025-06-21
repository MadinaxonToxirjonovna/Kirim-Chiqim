from collections import defaultdict

import logging
from decimal import Decimal
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from profil.models import Profil
from .models import Kirim, Chiqim, Valyuta, Kimdan, Uchun
from .forms import HisobFilterForm, ChiqimForm, KirimForm, ValyutaForm, UchunForm, KimdanForm, ValyutaKursiForm
from django.utils import timezone

logger = logging.getLogger(__name__)


def is_user_profile_completed(user):
    """
    Foydalanuvchi profilining to'liq to'ldirilganligini tekshiradi.
    Agar profil to'liq bo'lmasa, False qaytaradi.
    """
    try:
        profile = Profil.objects.get(user=user)
        return profile.is_profile_completed
    except Profil.DoesNotExist:
        return False



def hisob(request):
    valyutalar = Valyuta.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    valyuta_id = request.GET.get('valuta')

    kirimlar = Kirim.objects.all()
    chiqimlar = Chiqim.objects.all()

    if start_date:
        kirimlar = kirimlar.filter(sana__gte=start_date)
        chiqimlar = chiqimlar.filter(sana__gte=start_date)
    if end_date:
        kirimlar = kirimlar.filter(sana__lte=end_date)
        chiqimlar = chiqimlar.filter(sana__lte=end_date)
    if valyuta_id:
        kirimlar = kirimlar.filter(valuta__id=valyuta_id)
        chiqimlar = chiqimlar.filter(valuta__id=valyuta_id)

    jami_kirim = kirimlar.aggregate(Sum('summa'))['summa__sum'] or 0
    jami_chiqim = chiqimlar.aggregate(Sum('summa'))['summa__sum'] or 0
    balans = jami_kirim - jami_chiqim

    valuta = None
    if valyuta_id:
        valuta = Valyuta.objects.filter(id=valyuta_id).first()

    context = {
        'valyutalar': valyutalar,
        'jami_kirim': jami_kirim,
        'jami_chiqim': jami_chiqim,
        'balans': balans,
        'valuta': valuta,
        'kirimlar': kirimlar,
        'chiqimlar': chiqimlar,
    }
    return render(request, 'transactions/hisob.html', context)




@login_required
def kirim_qosh(request):
    if not is_user_profile_completed(request.user):
        messages.error(request, "Profilingiz to'liq emas. Iltimos, avval profilingizni to'ldiring.")
        return redirect('profil:complete_profile')

    if request.method == 'POST':
        form = KirimForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                kirim = form.save(commit=False)
                kirim.user = request.user
                kirim.save()
                messages.success(request, "Kirim muvaffaqiyatli qo'shildi!")
                return redirect('transactions:hisob')
            except Exception as e:
                messages.error(request, f"Kirimni qo'shishda xato yuz berdi: {e}")
                logger.error(f"Kirimni saqlashda xato: {e}", exc_info=True) 
        else:
            messages.error(request, "Kirimni qo'shishda xato. Iltimos, formani to'g'ri to'ldiring.")
            logger.error(f"Kirim formasida xato: {form.errors}", exc_info=True) 

    else: 
        form = KirimForm(user=request.user)

    return render(request, "transactions/kirim_qosh.html", {'form': form})



@login_required
def chiqim_qosh(request):
    if not is_user_profile_completed(request.user):
        messages.error(request, "Profilingiz to'liq emas.")
        return redirect('profil:complete_profile')

    if request.method == 'POST':
        form = ChiqimForm(request.POST, user=request.user)  
        if form.is_valid():
            chiqim = form.save(commit=False)
            chiqim.user = request.user
            chiqim.save()
            messages.success(request, "Chiqim muvaffaqiyatli qo'shildi!")
            return redirect('transactions:hisob')
        else:
            messages.error(request, "Formada xatolik bor.")
    else:
        form = ChiqimForm(user=request.user) 

    return render(request, "transactions/chiqim_qosh.html", {'form': form})




@login_required
def valyuta_qosh(request):
    if not is_user_profile_completed(request.user):
        messages.error(request, "Profilingiz to'liq emas. Iltimos, avval profilingizni to'ldiring.")
        return redirect('profil:complete_profile')

    if request.method == 'POST':
        form = ValyutaForm(request.POST) 
        if form.is_valid():
            try:
                valyuta = form.save(commit=False)
                valyuta.user = request.user 
                valyuta.save()
                messages.success(request, "Valyuta muvaffaqiyatli qo'shildi!")
                return redirect('transactions:hisob')
            except Exception as e:
                messages.error(request, f"Valyutani qo'shishda xato yuz berdi: {e}")
                logger.error(f"Valyutani saqlashda xato: {e}", exc_info=True)
        else:
            messages.error(request, "Valyutani qo'shishda xato. Iltimos, formani to'g'ri to'ldiring.")
            logger.error(f"Valyuta formasida xato: {form.errors}", exc_info=True)
    else:
        form = ValyutaForm()
    return render(request, "transactions/valyuta_qosh.html", {'form': form})


@login_required
def uchun_qosh(request):
    try:
        pr = Profil.objects.filter(user=request.user).first()
        if not pr.is_login:
            return redirect('profil:login')

        if request.method == 'POST':
            form = UchunForm(request.POST)
            if form.is_valid():
                uchun = form.save(commit=False)
                uchun.user = request.user
                uchun.save()
                return redirect('kirim:chiqim_qosh')
        else:
            form = UchunForm()

        return render(request, 'uchun_qosh.html', {'form': form})
    except Exception as e:
        messages.error(request, f"'Uchun' qo'shishda xatolik yuz berdi: {e}")
        return redirect('transactions:chiqim_qosh')

@login_required
def kimdan_qosh(request):
    if not is_user_profile_completed(request.user):
        messages.error(request, "Profilingiz to'liq emas. Iltimos, avval profilingizni to'ldiring.")
        return redirect('profil:complete_profile')

    if request.method == 'POST':
        form = KimdanForm(request.POST)
        if form.is_valid():
            try:
                kimdan = form.save(commit=False)
                kimdan.user = request.user
                kimdan.save()
                messages.success(request, "Manba muvaffaqiyatli qo'shildi!")
                return redirect("transactions:kirim_qosh")
            except Exception as e:
                messages.error(request, f"Manbani qo'shishda xato yuz berdi: {e}")
                logger.error(f"Manbani saqlashda xato: {e}", exc_info=True)
        else:
            messages.error(request, "Manbani qo'shishda xato. Iltimos, formani to'g'ri to'ldiring.")
            logger.error(f"Kimdan formasida xato: {form.errors}", exc_info=True)

    else:
        form = KimdanForm()
    return render(request, "transactions/kimdan_qosh.html", {'form': form}) 
  

@login_required
def kurs_kirit(request):
    try:
        pr = Profil.objects.filter(user=request.user).first()
        if not pr.is_login:
            return redirect('profil:login')

        if request.method == 'POST':
            form = ValyutaKursiForm(request.POST, user=request.user)
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

                jami_kirim, jami_chiqim = Decimal(0), Decimal(0)
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

                return render(request, 'kurs_natija.html', {
                    'asosiy': asosiy,
                    'kurslar_qiymatlari': kurslar_qiymatlari,
                    'jami_kirim': round(jami_kirim, 2),
                    'jami_chiqim': round(jami_chiqim, 2),
                    'balans': round(balans, 2),
                })

        else:
            form = ValyutaKursiForm(user=request.user)

        return render(request, 'kurs_kirit.html', {'form': form})
    except Exception as e:
        messages.error(request, f"Kurslarni kiritishda xatolik yuz berdi: {e}")
        return redirect('transactions:kurs_kirit')

@login_required
def kirim(request):
    try:
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
            dic[i.short] = dic.get(i.short, 0) + kv

        context = {
            'kirimlar': kirimlar,
            'jami_kirim': jami_kirim,
            'valyutalar': val_k,
            'kimdan_choices': kimdan_choices,
            'valuta': Valyuta.objects.get(id=valuta) if valuta else None,
            'dic': dic,
            'form': request.GET,
        }
        return render(request, 'kirim.html', context)
    except Exception as e:
        messages.error(request, f"Kirimlarni ko'rsatishda xatolik yuz berdi: {e}")
        return redirect('transactions:hisob')

@login_required
def chiqim(request):
    if not is_user_profile_completed(request.user):
        messages.error(request, "Profilingiz to'liq emas. Iltimos, avval profilingizni to'ldiring.")
        return redirect('profil:complete_profile')

    filter_form = HisobFilterForm(request.GET, user=request.user) 
    chiqimlar = Chiqim.objects.filter(user=request.user).order_by('-sana')

    if filter_form.is_valid():
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')
        valuta = filter_form.cleaned_data.get('valuta')

        if start_date:
            chiqimlar = chiqimlar.filter(sana__gte=start_date)
        if end_date:
            chiqimlar = chiqimlar.filter(sana__lte=end_date)
        if valuta:
            chiqimlar = chiqimlar.filter(valuta=valuta)

    jami = chiqimlar.aggregate(Sum('summa'))['summa__sum'] or Decimal(0) 
    return render(request, 'transactions/chiqim.html', {'chiqimlar': chiqimlar, 'jami_chiqim': jami, 'filter_form': filter_form})