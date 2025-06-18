from django import forms
from transactions.models import Chiqim, Kirim, Valyuta, Uchun, Kimdan
from .models import Kirim, Kimdan, Valyuta 
from django.forms.widgets import DateInput

class HisobFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    end_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)

class KirimForm(forms.ModelForm):
    class Meta:
        model = Kirim
        fields = ['sana', 'summa', 'kimdan', 'valuta', 'izoh']
        widgets = {
            'sana': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'summa': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Miqdor kiriting'}),
            'kimdan': forms.Select(attrs={'class': 'form-select'}),
            'valuta': forms.Select(attrs={'class': 'form-select'}),
            'izoh': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Qo‘shimcha ma’lumot yozing...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['kimdan'].queryset = Kimdan.objects.filter(user=user)
            self.fields['valuta'].queryset = Valyuta.objects.filter(user=user)
        else:
            self.fields['kimdan'].queryset = Kimdan.objects.none()
            self.fields['valuta'].queryset = Valyuta.objects.none()


class ChiqimForm(forms.ModelForm):
    class Meta:
        model = Chiqim
        fields = ['uchun', 'sana', 'summa', 'summa_type', 'valuta', 'izoh']
        widgets = {
            'sana': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'summa': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'summa_type': forms.Select(attrs={'class': 'form-select'}),
            'valuta': forms.Select(attrs={'class': 'form-select'}),
            'uchun': forms.Select(attrs={'class': 'form-select'}),
            'izoh': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user') 
        super().__init__(*args, **kwargs)
        self.fields['uchun'].queryset = Uchun.objects.filter(user=user)
        self.fields['valuta'].queryset = Valyuta.objects.filter(user=user)


class ValyutaForm(forms.ModelForm):
    class Meta:
        model = Valyuta
        fields = ['name', 'short']


class UchunForm(forms.ModelForm):
    class Meta:
        model = Uchun
        fields = ['nomi', ]


class KimdanForm(forms.ModelForm):
    class Meta:
        model = Kimdan
        fields = ['nomi', ]


class ValyutaKursiForm(forms.Form):
    asosiy_valyuta = forms.ModelChoiceField(queryset=Valyuta.objects.none(), label="Asosiy valyuta")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['asosiy_valyuta'].queryset = Valyuta.objects.filter(user=user)
        valyutalar = Valyuta.objects.filter(user=user)

        for val in valyutalar:
            self.fields[f'kurs_{val.id}'] = forms.DecimalField(
                label=f"1 {val.short} = ",
                required=False,
                decimal_places=7
            )