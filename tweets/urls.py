"""Mappings from URLs to views"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create_post/', views.create_post, name='tweets-create_post'),
    path('vote/', views.vote, name="tweets-vote"),
    path('filter_posts/', views.FilterView.as_view(), name='tweets-filter_posts'),
    path('logout/', views.safe_logout, name='safe_logout'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete-post'),
    path('post/<int:pk>', views.PostView.as_view(), name='post_page'),
    path("<str:username>/", views.ProfileView.as_view(), name='user_profile'),

]
