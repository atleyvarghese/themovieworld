from django.contrib.auth.models import User
from django.db import models
from allauth.account.signals import user_signed_up,user_logged_in
from django.dispatch import receiver


class UserProfile(models.Model):
    user   = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    profile_picture_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.username






@receiver(user_logged_in)
def user_signed_up_(request, user, sociallogin=None, **kwargs):
        profile = UserProfile.objects.get_or_create(user=user)
            # Extract first / last names from social nets and store on User record
        if sociallogin:
            print("inside if 1----------------------------")
            if user.socialaccount_set.filter(provider='Facebook'):
                extra_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
                if extra_data:
                    id = extra_data['id']
                    if id:
                        profile[0].profile_picture_url = "http://graph.facebook.com/{0}/picture?type=large".format(id)
                        profile[0].save()
            if user.socialaccount_set.filter(provider='google'):
                print("inside if 2----------------------------")
                extra_data = user.socialaccount_set.filter(provider='google')[0].extra_data
                print(extra_data)
                if extra_data:
                    id = extra_data['id']
                    if id:
                        profile[0].profile_picture_url = extra_data['picture']
                        profile[0].save()
