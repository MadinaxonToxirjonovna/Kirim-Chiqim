from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from transactions.models import Chiqim, Kirim, Valyuta, Kimdan, Uchun
from profil.models import Profil
from .serializers import ProfilSerializer, ChiqimSerializer, KirimSerializer, ValyutaSerializer, KimdanSerializer, \
    UchunSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer


class ProfilListCreateAPIView(generics.ListCreateAPIView):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfilRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': response.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logout bo‘ldi."}, status=status.HTTP_200_OK)


class UchunListCreateAPIView(generics.ListCreateAPIView):
    queryset = Uchun.objects.all()
    serializer_class = UchunSerializer
    permission_classes = [IsAuthenticated]


class UchunDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Uchun.objects.all()
    serializer_class = UchunSerializer
    permission_classes = [IsAuthenticated]


class KimdanListCreateAPIView(generics.ListCreateAPIView):
    queryset = Kimdan.objects.all()
    serializer_class = KimdanSerializer
    permission_classes = [IsAuthenticated]


class KimdanDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kimdan.objects.all()
    serializer_class = KimdanSerializer
    permission_classes = [IsAuthenticated]


class ValyutaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Valyuta.objects.all()
    serializer_class = ValyutaSerializer
    permission_classes = [IsAuthenticated]


class ValyutaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Valyuta.objects.all()
    serializer_class = ValyutaSerializer
    permission_classes = [IsAuthenticated]


class KirimListCreateAPIView(generics.ListCreateAPIView):
    queryset = Kirim.objects.all()
    serializer_class = KirimSerializer
    permission_classes = [IsAuthenticated]


class KirimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Kirim.objects.all()
    serializer_class = KirimSerializer
    permission_classes = [IsAuthenticated]


class ChiqimListCreateAPIView(generics.ListCreateAPIView):
    queryset = Chiqim.objects.all()
    serializer_class = ChiqimSerializer
    permission_classes = [IsAuthenticated]


class ChiqimDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chiqim.objects.all()
    serializer_class = ChiqimSerializer
    permission_classes = [IsAuthenticated]
