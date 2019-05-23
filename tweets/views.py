from django.shortcuts import render
from .models import Post, Vote
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.core.exceptions import PermissionDenied


class CreatePostForm(forms.Form):
    post_text = forms.CharField(widget=forms.Textarea( \
        attrs={"rows":10, "cols":60}), label='Tweet away', required=True)

# this class is not used at the moment (consider refactor?)
class LoginForm(forms.Form):
    username = forms.CharField(label="User name", required="True")
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput())


def index(request):
    """View function for home page of site."""

    all_posts = Post.objects.all()

    context = {
        'posts': all_posts
    }

    return render(request, 'index.html', context=context)


@login_required
def create_post(request):

    if request.method == "POST":
        filled_out_form = CreatePostForm(request.POST)
        if filled_out_form.is_valid():
            post_text = filled_out_form.cleaned_data['post_text']
            post = Post.objects.create(text=post_text, author=request.user)
            return render(request, 'index.html')
        else:
            # handle this
            pass
    else:
        create_post_form = CreatePostForm()

    return render(request, 'create_post_form.html', {'form': create_post_form})


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


def login(request):
    # todo: log user in

    # change this
    return render(request, 'index.html', {'message': 'logged in'})


def logout(request):
    # todo: log user out

    # change this
    return render(request, 'index.html', {'message': 'logged out'})
