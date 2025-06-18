from django.contrib.auth import logout, login, authenticate
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfilForm, CustomUserCreationForm
from .models import Profil
from .utils import generate_verification_code
from django.contrib import messages


@login_required
def profil(request):
    pr = Profil.objects.filter(user=request.user).first()
    if not pr.is_login:
        return redirect('profil:login')
    profil = Profil.objects.filter(user=request.user).first()
    return render(request, 'profile.html', {'profil': profil})


@login_required
def tahrirlash(request):
    pr = Profil.objects.filter(user=request.user).first()
    if not pr.is_login:
        return redirect('profil:login')
    try:
        profil = Profil.objects.filter(user=request.user).first()
    except Profil.DoesNotExist:
        messages.error(request, "Profil topilmadi")
        return

    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi.")
            return redirect('profil:profil')
        else:
            messages.error(request, "Profilni yangilashda xatolik yuz berdi.")
    else:
        form = ProfilForm(instance=profil)

    return render(request, 'tahrir.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            kod = generate_verification_code()

            profil, created = Profil.objects.get_or_create(user=user)
            profil.tasdiqla_kod = kod
            profil.save()

            if user.email:
                send_code(user.email, kod)
                messages.success(request, f"Tasdiqlash kodi emailingizga yuborildi. ")
            elif profil.telefon:
                messages.success(request, "Tasdiqlash kodi telefoningizga yuborildi .")
            else:
                messages.warning(request, "Tasdiqlash kodi yuborilmadi: email yoki telefon topilmadi.")

            return redirect('profil:verify')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def send_code(user_email, code):
    subject = 'Tasdiqlash kodi'
    message = f"Sizning tasdiqlash kodingiz: {code}"
    from_email = 'madinaxontoxirjonovna@gmail.com'
    send_mail(subject, message, from_email, [user_email], fail_silently=False)
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            code = generate_verification_code()
            profil = Profil.objects.filter(user=user).first()
            profil.tasdiqla_kod = code
            profil.save()

            if user.email:
                send_code(user.email, code)
            elif profil.telefon:
                print(f"Telefon uchun kod: {code}")
                messages.success(request, f'Login muvaffaqiyatli. Tasdiqlash kodi yuborildi!  {code}')
                return redirect('profil:verify')
            else:
                messages.error(request, f'Login yoki parol noto‘g‘ri!')
    return render(request, 'login.html')


def verify_view(request):
    if request.method == 'POST':
        kod = request.POST.get('kod')
        profil = Profil.objects.filter(user=request.user).order_by('-kod_vaqt').first()

        if profil.tasdiqla_kod == kod:
            messages.success(request, "Tasdiqlash muvaffaqiyatli.")
            profil.is_login = True
            profil.save()
            return redirect('profil:profil')
        else:
            messages.error(request, "Kod noto‘g‘ri.")
    return render(request, 'verify.html')


@login_required
def logout_view(request):
    pr = Profil.objects.filter(user=request.user).first()
    if pr:
        pr.is_login = False
        pr.save()
    logout(request)
    return redirect('profil:login') 

@login_required
def complete_profile(request):
    profil = Profil.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            profil = form.save(commit=False)
            profil.is_profile_completed = True 
            profil.save()
            return redirect('profil:profil')
    else:
        form = ProfilForm(instance=profil)

    return render(request, 'tahrir.html', {'form': form})
