from django.contrib.auth.models import User
from rest_framework import serializers
from twilio.rest import Client

import random

from .models import Profile
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        extra_kwargs = {
            'username': {'write_only': True},
            'email': {'write_only': True}
        }

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        if password1 != password2:
            raise serializers.ValidationError({'error': 'Пароли не совпадают.'})
        user = User(**validated_data)
        user.set_password(password1)
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'telephone', 'verification', 'role']
        extra_kwargs = {'verification': {'read_only': True}}

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        verification_code = generate_verification_code()

        profile = Profile.objects.create(
            user=user,
            telephone=validated_data['telephone'],
            verification_token=verification_code,
            role=validated_data.get('role', 'user')
        )
        send_verification_sms(profile.telephone, verification_code)
        return profile


def generate_verification_code():
    return str(random.randint(100000, 999999))


def send_verification_sms(phone_number, code):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)
    try:
        # Отправка SMS через Twilio
        message = client.messages.create(
            body=f'Ваш код подтверждения: {code}',
            from_=twilio_phone_number,
            to=phone_number
        )
        print(f'SMS отправлено на {phone_number}. SID: {message.sid}')
    except Exception as e:
        print(f'Не удалось отправить SMS: {e}')
        raise Exception('Не удалось отправить SMS')
