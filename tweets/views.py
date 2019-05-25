from django.shortcuts import render
from .models import Post, Vote
from .forms import CreatePostForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_protect
#from axes.models import AccessLog

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

@csrf_protect
@require_http_methods(["POST"])
def safe_logout(request):
    logout(request)
    return HttpResponseRedirect("/")
