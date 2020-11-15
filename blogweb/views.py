from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile, Comment, PostComment 
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, PostCreatedForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    posts = Post.objects.all()
    
    context = {
        'posts': posts
    }
    return render(request, 'blogweb/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blogweb/home.html'
    context_object_name = 'posts'
    ordering = ['-date_created']
    paginate_by = 3

def register_page(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            return redirect("/")
    context = {
        'form': form
    }
    return render(request, 'blogweb/register.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Your username or password is incorrcect')

    return render(request, 'blogweb/login.html')

def logout_page(request):
    logout(request)
    return redirect('login')

def profile(request):
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile is updates')
            return redirect('profile')

    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blogweb/profile.html', context)

def post_created(request):
    form = PostCreatedForm()

    if request.method == 'POST':
        form = PostCreatedForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            post = Post.objects.create(title=title, content=content, author=request.user)
            return redirect('home')


    context = {
        'form': form
    }
    return render(request, 'blogweb/create-post.html', context)
@login_required(login_url='login')
def post_detail(request, id):
    post = Post.objects.get(id=id)
    post_comment, created = PostComment.objects.get_or_create(post=post)
    all_comment = PostComment.objects.get(post=post)
    print("post: ", all_comment)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            content = form.cleaned_data.get('comment')
            comment = Comment.objects.create(comment=content, user=user)
            comment.save()
            
            post_comment.comment.add(comment)
            post_comment.save()
            return redirect('post-detail', id=id)

    context = {
        'post': post,
        'form': form, 
        'all_comment': all_comment
    }

    return render(request, 'blogweb/post-detail.html', context)

def post_update(request, id):
    post = Post.objects.get(author=request.user, id=id)
    form = PostCreatedForm(instance=post)
    
    if request.method == 'POST':
        form = PostCreatedForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'blogweb/post-update.html', context)

def post_delete(request, id):
    post = Post.objects.get(author=request.user, id=id)
    context = {
        'post': post
    }
    post.delete()
    return redirect('home')

class UserPostListView(ListView):
    model = Post
    template_name = 'blogweb/author-post.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user)

#dung cach nay cung dc nhung phai viet them code paginator
def author_post(request, username):
    user = User.objects.get(username=username)
    print(user)
    posts = Post.objects.filter(author=user)
    
    context = {
        'posts': posts
    }
    return render(request, 'blogweb/author-post.html', context)

