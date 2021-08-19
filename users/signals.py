from django.dispatch import receiver
import requests
from django.core import files
from io import BytesIO
from .models import SocialflyUser
from allauth.account.signals import user_signed_up



@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):
    extra_data=user.socialaccount_set.filter(provider='google')[0].extra_data
    resp = requests.get(extra_data['picture'])
    fp = BytesIO()
    fp.write(resp.content)
    file_name = extra_data['picture'].split("/")[-1]
    socialflyuser = SocialflyUser.objects.create(user=user)
    socialflyuser.profile_photo.save(user.username+'.png', files.File(fp))
    socialflyuser.save()