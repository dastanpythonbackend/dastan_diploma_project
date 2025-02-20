from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError

from .serializers import UserSerializer, ProfileSerializer
from .models import Profile


class ProfileView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(APIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'message': 'Пользователь зарегистрирован. Код подтверждения отправлен через SMS.'},
            status=status.HTTP_201_CREATED)


class VerifySMSView(APIView):
    def post(self, request):
        phone_number = request.data.get('telephone')
        code = request.data.get('code')
        if not phone_number or not code:
            raise ValidationError({'error': 'Телефон и код обязательны.'})
        try:
            profile = Profile.objects.get(telephone=phone_number)
        except Profile.DoesNotExist:
            raise NotFound({'error': 'Пользователь не найден.'})
        if profile.verification_token != code:
            raise ValidationError({'error': 'Неверный код подтверждения.'})
        profile.verification = True
        profile.verification_token = None
        profile.save()

        return Response({'message': 'Номер телефона успешно верифицирован.'}, status=status.HTTP_200_OK)
