from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib import messages
from django.utils.timesince import timesince

from useraudit.models import LoginLog

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    try:
        previous_login = LoginLog.objects.filter(username__exact=user.username).order_by('-timestamp')[1]
        previous_login_time = timesince(previous_login.timestamp)
        messages.add_message(request, messages.INFO, f"Welcome back {user.username}! You previusly logged in {previous_login_time} ago from {previous_login.ip_address} with {previous_login.user_agent}")
    except IndexError:
        # User has logged in for the first time: an "account created" page is shown,
        # so no need to set a message
        pass

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    messages.add_message(request, messages.INFO, 'You have been logged out.')
