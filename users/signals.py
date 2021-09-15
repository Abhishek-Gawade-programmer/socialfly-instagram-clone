from django.dispatch import receiver
import requests
from django.core import files
from io import BytesIO
from .models import SocialflyUser
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):
    url=f'https://ui-avatars.com/api/?name={user.first_name}+{user.last_name}&size=256&bold=true&background=random'
    response = requests.get(url)
    fp = BytesIO()  
    fp.write(response.content)
    socialflyuser = SocialflyUser.objects.create(user=user)
    socialflyuser.profile_photo.save(user.username+'.png', files.File(fp))
    socialflyuser.save()