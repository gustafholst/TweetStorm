from django.shortcuts import render
from .models import Post, Vote
from .forms import CreatePostForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.views import LoginView
from django.db.utils import IntegrityError

from django_registration.backends.one_step.views import RegistrationView
from ratelimit.decorators import ratelimit
from ratelimit.mixins import RatelimitMixin

import json

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
@ratelimit(key='user', rate='5/m', block=True)
def create_post(request):
    filled_out_form = CreatePostForm(request.POST)
    if filled_out_form.is_valid():
        post_text = filled_out_form.cleaned_data['post_text']
        post = Post.objects.create(text=post_text, author=request.user)
        messages.add_message(request, messages.INFO, 'Tweet successfully tweeted!')
    else:
        messages.add_message(request, messages.WARNING, 'Form data invalid.')

    return HttpResponseRedirect("/")


def filter_posts(request):
    filtered_posts = Post.objects.none()

    if request.GET.get('user'):
        filtered_posts = Post.objects.filter(author__username=request.GET['user'])

    if request.GET.get('word'):
        filtered_posts = Post.objects.filter(text__icontains=request.GET['word'])

    return render(request, 'index.html', {'posts': filtered_posts })


@login_required
@require_http_methods(["POST"])
def delete_post(request):
    post_id = request.POST.get('post_id')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    if request.user == post.author:
        post.delete()
        messages.add_message(request, messages.INFO, 'Tweet was deleted')
    else:
        messages.add_message(request, messages.WARNING, 'You are not authorized to delete this tweet')

    return HttpResponseRedirect("/")


@require_http_methods(["POST"])
def vote(request):
    post_id = request.POST.get('post_id')
    vote = request.POST.get('vote')

    response = {}

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    try:
        post.vote_set.create(vote=vote, voter=request.user)
        response['message'] = "Tweet upvoted"
    except IntegrityError:
        post.vote_set.filter(voter=request.user).update(vote=vote)
        response['message'] = "Vote updated"

    response['post_id'] = post.id
    response['num_up_votes'] = post.num_up_votes
    response['num_down_votes'] = post.num_down_votes

    return HttpResponse(json.dumps(response),
                        content_type='application/json')

@csrf_protect
@require_http_methods(["POST"])
def safe_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def username_and_ip(group, request):
    return f"{request.POST.get('username')}:{request.META['REMOTE_ADDR']}"

class CustomLoginView(RatelimitMixin, LoginView):
    ratelimit_key = username_and_ip
    ratelimit_rate = '5/h'
    ratelimit_block = True
    ratelimit_method = 'POST'

class CustomRegistrationView(RatelimitMixin, RegistrationView):
    ratelimit_key = 'ip'
    ratelimit_rate = '5/h'
    ratelimit_block = True
    ratelimit_method = 'POST'

def rate_limited(request, exception):
    return render(request, 'rate_limited.html', {'error': 'Too much, too soon. You\'ve been throttled.'})
