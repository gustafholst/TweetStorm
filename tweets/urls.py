from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create_post/', views.create_post, name='tweets-create_post'),
    path('delete_post/', views.delete_post, name='tweets-delete_post'),
    path('voteup/', views.vote_up, name="tweets-vote_up"),
    path('votedown/', views.vote_down, name="tweets-vote_down"),
    path('filter_posts/', views.filter_posts, name="tweets-filter_posts"),
    path('logout/', views.safe_logout, name="safe_logout"),
    path('post/<int:pk>', views.PostView.as_view(), name="post_page"),
    path("<str:username>/", views.ProfileView.as_view(), name="user_profile"),
]
