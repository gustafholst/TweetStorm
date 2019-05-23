from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_post/', views.create_post, name='tweets-create_post'),
    path('delete_post/', views.delete_post, name='tweets-delete_post'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout")
]
