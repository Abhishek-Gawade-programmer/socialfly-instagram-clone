from django import template
from  users.models import *
from  posts.models import *

from django.shortcuts import get_object_or_404
register = template.Library()

@register.filter
def check_follow_or_unfollow(receiver_id,sender_id):
    receiver_user = get_object_or_404(SocialflyUser, pk = receiver_id)

    return receiver_user.allow_to_follow(sender_id)

@register.filter
def check_like_post(user_id,post_id):
    post = get_object_or_404(Post, pk = post_id)
    user = get_object_or_404(User, pk = user_id)
    if user in post.like_people.all():
        return True
    return False

