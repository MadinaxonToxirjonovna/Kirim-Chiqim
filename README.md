# 💸 Kirim-Chiqim

**Kirim-Chiqim** — bu shaxsiy yoki biznes moliyaviy harajatlar va tushumlarni boshqarish uchun mo‘ljallangan Django asosidagi veb-ilova. Foydalanuvchi tizimga kirgach, o‘z kirim va chiqimlarini, valyuta konversiyasini, va hisobotlarni boshqarishi mumkin.



## 🧩 Loyihaning asosiy imkoniyatlari

 🔐 Foydalanuvchi ro‘yxatdan o‘tishi, kirishi va profilingini to‘ldirishi
 ➕ Kirim qo‘shish
 ➖ Chiqim qo‘shish
 💱 Valyuta turlari va kurslarini kiritish
 📊 Hisobotlarni vaqt bo‘yicha filtrlash
 🔍 Qayerdan (Kimdan) va Nima uchun (Uchun) orqali filtrlash
 🧾 PDF yoki grafik ko‘rinishdagi hisobot (bo‘lajak imkoniyat)



## ⚙️ Texnologiyalar

- **Backend**: Django 5.x
- **Frontend**: Bootstrap 5 (jQuery va Tailwind qo‘llab-quvvatlanadi)
- **Ma'lumotlar bazasi**: SQLite (asosiy), PostgreSQL (opsional)
- **Autentifikatsiya**: Django auth + Profil to‘ldirish tekshiruvi
- **API**: DRF (agar REST API yozilgan bo‘lsa)
- **Versiya nazorati**: Git & GitHub



## 🚀 O‘rnatish (Local serverda)

```bash
# 1. Loyihani yuklab oling
git clone https://github.com/MadinaxonToxirjonovna/Kirim-Chiqim.git
cd Kirim-Chiqim

# 2. Virtual muhit yarating
python -m venv .env
source .env/bin/activate    # (Linux/macOS)
.env\Scripts\activate       # (Windows)

# 3. Talablar faylidan kutubxonalarni o‘rnating
pip install -r requirements.txt

# 4. Migratsiyalarni bajaring
python manage.py migrate

# 5. Superuser yarating (admin panel uchun)
python manage.py createsuperuser

# 6. Serverni ishga tushiring
python manage.py runserver

👩‍💻 Muallif
Ism: Madinaxon Toxirjonovna
Telegram: @MToxirjonovna
GitHub: MadinaxonToxirjonovna
Email: madinaxontoxirjonovna@gmail.com