from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True,null=True)
    verification_count = models.IntegerField(default=0)
    telephone = models.CharField(max_length=20)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
