from django import template
from  users.models import SocialflyUser
from django.shortcuts import get_object_or_404
register = template.Library()
@register.filter
def check_follow_or_unfollow(receiver_id,sender_id):
    receiver_user = get_object_or_404(SocialflyUser, pk = receiver_id)
    print(receiver_user.allow_to_follow(sender_id))

    return receiver_user.allow_to_follow(sender_id)
    # sender_user = get_object_or_404(SocialflyUser, pk = receiver_id)


