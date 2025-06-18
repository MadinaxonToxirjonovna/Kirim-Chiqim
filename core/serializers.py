from rest_framework import serializers

from transactions.models import Chiqim, Valyuta, Uchun, Kimdan, Kirim
from profil.models import Profil
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfilSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profil
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UchunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uchun
        fields = ['id', 'nomi']


class KimdanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kimdan
        fields = ['id', 'nomi']


class ValyutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valyuta
        fields = ['id', 'name', 'short']


class KirimSerializer(serializers.ModelSerializer):
    kimdan = KimdanSerializer()
    valuta = ValyutaSerializer()

    class Meta:
        model = Kirim
        fields = ['id', 'kimdan', 'sana', 'summa', 'summa_type', 'valuta', 'izoh']

    def create(self, validated_data):
        kimdan_data = validated_data.pop('kimdan')
        kimdan = Kimdan.objects.create(**kimdan_data)
        valuta_data = validated_data.pop('valuta')
        valuta = Valyuta.objects.create(**valuta_data)
        kirim = Kirim.objects.create(kimdan=kimdan, valuta=valuta, **validated_data)
        return kirim


class ChiqimSerializer(serializers.ModelSerializer):
    uchun = UchunSerializer()
    valuta = ValyutaSerializer()

    class Meta:
        model = Chiqim
        fields = ['id', 'uchun', 'sana', 'summa', 'summa_type', 'valuta', 'izoh']

    def create(self, validated_data):
        uchun_data = validated_data.pop('uchun')
        uchun = Uchun.objects.create(**uchun_data)
        valuta_data = validated_data.pop('valuta')
        valuta = Valyuta.objects.create(**valuta_data)
        chiqim = Chiqim.objects.create(uchun=uchun, valuta=valuta, **validated_data)
        return chiqim
