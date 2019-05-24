from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_post/', views.create_post, name='tweets-create_post'),
    path('delete_post/', views.delete_post, name='tweets-delete_post'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('voteup/', views.vote_up, name="tweets-vote_up"),
    path('votedown/', views.vote_down, name="tweets-vote_down"),
    path('filter_posts/', views.filter_posts, name="tweets-filter_posts"),
]
