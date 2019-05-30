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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tweets.views import IndexView, CustomLoginView, CustomRegistrationView, AccountSecurityView
from two_factor.urls import urlpatterns as tf_urls
from django_registration.forms import RegistrationFormUniqueEmail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweets/', include('tweets.urls')),
    path('account/login/', CustomLoginView.as_view(), name='login'),
    path('account/', include('django_registration.backends.one_step.urls')),
    path('account/',
         CustomRegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
         name='django_registration_register'),
    path('account/change-password/',
         auth_views.PasswordChangeView.as_view(
             template_name='registration/change_password_form.html',
             success_url='/accounts/change-password/done/'),
         name='change_password'),
    path('account/change-password/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/change_password_done.html'),
         name='change_password_done'),
    path('account/two_factor/',
         AccountSecurityView.as_view(),
         name='account_security'),
    path('', include(tf_urls)),
    path('', IndexView.as_view()),
    path('account/reset-password',
         auth_views.PasswordResetView.as_view(
             template_name='registration/send_email_form.html',
             html_email_template_name='registration/reset_email.html'),
         name='reset_password'),
    path('account/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/reset_password_form.html'),
         name='password_reset_confirm'),
    path('account/password_reset_done',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/reset_password_done.html'),
         name='password_reset_done'),
    path('account/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/reset_password_complete.html'),
         name='password_reset_complete'),
]
