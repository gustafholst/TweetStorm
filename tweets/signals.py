"""Callback functions to handle various signals."""
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib import messages
from django.utils.timesince import timesince

from useraudit.models import LoginLog


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """Adds a message when a user logs in."""
    try:
        previous_login = LoginLog.objects.filter(
            username__exact=user.username).order_by('-timestamp')[1]
        previous_login_time = timesince(previous_login.timestamp)
        message = (
            f"Welcome back {user.username}! You previously logged in "
            f"{previous_login_time} ago from {previous_login.ip_address} "
            f"with {previous_login.user_agent}"
        )
        messages.add_message(request, messages.INFO, message)
    except IndexError:
        # User has logged in for the first time: an "account created" page is
        # shown, so no need to set a message
        pass


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """Adds a message when a user logs out."""
    messages.add_message(request, messages.INFO, 'You have been logged out.')
