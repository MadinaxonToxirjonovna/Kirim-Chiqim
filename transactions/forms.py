from django import forms

from transactions.models import Chiqim, Kirim, Valyuta, Uchun, Kimdan


class HisobFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    end_date = forms.DateField(widget=forms.SelectDateWidget(), required=False)



class KirimForm(forms.ModelForm):
    class Meta:
        model = Kirim
        fields = ['kimdan', 'sana', 'summa', 'summa_type', 'valuta', 'izoh']
        widgets = {
            'summa': forms.NumberInput(attrs={'step': '0.01'}),
            'sana': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['kimdan'].queryset = Kimdan.objects.filter(user=user)
        self.fields['valuta'].queryset = Valyuta.objects.filter(user=user)


class ChiqimForm(forms.ModelForm):
    class Meta:
        model = Chiqim
        fields = ['uchun', 'sana', 'summa', 'summa_type', 'valuta', 'izoh']
        widgets = {
            'summa': forms.NumberInput(attrs={'step': '0.01'}),
            'sana': forms.DateInput(attrs={'type': 'date'}),

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


class ValyutaKursForm(forms.Form):
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
