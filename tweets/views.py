from django.shortcuts import render, get_object_or_404
from .models import Post, Vote
from .forms import CreatePostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic import DeleteView

from django_registration.backends.one_step.views import RegistrationView
from ratelimit.decorators import ratelimit
from ratelimit.mixins import RatelimitMixin
from django.utils.decorators import method_decorator

import re

class IndexView(FormMixin, ListView):
    model = Post
    paginate_by = 10
    template_name ='index.html'
    form_class = CreatePostForm
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

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

class FilterView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'posts'
    template_name ='filtered.html'

    def get_queryset(self):
        filtered_posts = Post.objects.none()
        query = self.request.GET['query'] if 'query' in self.request.GET else ''

        if query:
            matches = re.search('(user:(?P<user>\w+))?\s?(?P<words>.*)?', query)
            if matches.group('user'):
                filtered_posts = Post.objects.filter(author__username=matches.group('user'))
                if matches.group('words'):
                    filtered_posts = filtered_posts.filter(text__icontains=matches.group('words'))
            elif matches.group('words'):
                filtered_posts = Post.objects.filter(text__icontains=matches.group('words'))

        return filtered_posts

    def get_context_data(self, **kwargs):
        context = super(FilterView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET['query'] if 'query' in self.request.GET else ''
        return context

@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        post = super(PostDeleteView, self).get_object()
        if not post.author == self.request.user:
            raise PermissionDenied
        return post

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

class ProfileView(ListView):
    model = Post
    paginate_by = 10
    template_name ='user_profile.html'

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return Post.objects.filter(author=user)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=self.kwargs['username'])
        return context

class PostView(DetailView):
    model = Post
