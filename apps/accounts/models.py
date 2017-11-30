from django.contrib.auth.models import User
from django.db import models
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


class UserProfile(models.Model):
    user   = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)





@receiver(user_signed_up)
def user_signed_up_(request, user, sociallogin=None, **kwargs):
        UserProfile.objects.create(user=user)
