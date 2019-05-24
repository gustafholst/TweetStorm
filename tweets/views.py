from django.shortcuts import render
from .models import Post, Vote
from .forms import CreatePostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.utils.timesince import timesince
from axes.models import AccessLog

def index(request):
    """View function for home page of site."""

    all_posts = Post.objects.all()

    context = {
        'form': CreatePostForm(),
        'posts': all_posts
    }

    return render(request, 'index.html', context=context)

@login_required
@require_http_methods(["POST"])
def create_post(request):
    filled_out_form = CreatePostForm(request.POST)
    if filled_out_form.is_valid():
        post_text = filled_out_form.cleaned_data['post_text']
        post = Post.objects.create(text=post_text, author=request.user)
        messages.add_message(request, messages.INFO, 'Tweet successfully tweeted!')
    else:
        messages.add_message(request, messages.WARNING, 'Form data invalid.')

    return HttpResponseRedirect("/")

def display_all_posts_by_user(request, user_id):
    all_posts = Post.objects.filter(author=user_id)

    return render(request, 'index.html', {'posts': all_posts })

@login_required
@require_http_methods(["POST"])
def delete_post(request):
    post_id = request.POST.get('post_id')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    if request.user is not post.author:
        raise PermissionDenied

    post.delete()

    return render(request, 'index.html', {'message': 'Tweet deleted'})


@login_required
@require_http_methods(["POST"])
def vote_up(request):
    post_id = request.POST.get('post_id')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    post.vote_set.create(vote=1, voter=request.user)

    return render(request, 'index.html', {'message': 'Tweet upvoted'})

@login_required
@require_http_methods(["POST"])
def vote_down(request):
    post_id = request.POST.get('post_id')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    post.vote_set.create(vote=-1, voter=request.user)

    return render(request, 'index.html', {'message': 'Tweet downvoted'})

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

        try:
            previous_login = AccessLog.objects.filter(username__exact=username).order_by('-attempt_time')[1]
            previous_login_time = timesince(previous_login.attempt_time)
            messages.add_message(request, messages.INFO, f"Welcome back {username}! You were last logged in {previous_login_time} ago from {previous_login.ip_address}")
        except IndexError:
            messages.add_message(request, messages.INFO, 'You are logged in!')
    else:
        messages.add_message(request, messages.WARNING, 'Incorrect combination username/password')

    return HttpResponseRedirect("/")

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Successfully logged out!')

    return HttpResponseRedirect("/")
