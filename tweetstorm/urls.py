"""tweetstorm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView
from django.urls import include
from django.contrib.auth import views as auth_views
from tweets.views import IndexView, CustomLoginView, CustomRegistrationView
from two_factor.urls import urlpatterns as tf_urls

# https://docs.djangoproject.com/en/2.2/topics/auth/default/#using-the-views
# path('accounts/', include('django.contrib.auth.urls')) includes the following:
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweets/', include('tweets.urls')),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', CustomRegistrationView.as_view(), name='django_registration_register'),
    #path('accounts/login/', auth_views.LoginView.as_view(), name='login'), # custom login view used for ratelimit mixin
    ###path('accounts/login/', CustomLoginView.as_view(), name='login'),
    #path('accounts/logout/', auth_views.LogoutView.as_view()), # we use our own view for this, as Django's default one lacks CSRF protection
    path('accounts/change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password_form.html', success_url='/accounts/change-password/done/'), name='change_password'),
    path('accounts/change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/change_password_done.html'), name='change_password_done'),
    path('', include(tf_urls)),
    path('', IndexView.as_view()),
    path("accounts/reset-password", auth_views.PasswordResetView.as_view(template_name='registration/send_email_form.html', html_email_template_name="registration/reset_email.html"), name="reset_password"),
    #path("accounts/password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("accounts/password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_password_form.html'), name="password_reset_confirm"),
    path("accounts/password_reset_done", auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_password_done.html'), name="password_reset_done"),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_password_complete.html'), name='password_reset_complete'),
    #path('', RedirectView.as_view(url='/tweets/', permanent=True)),
]
