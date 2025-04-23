from .models import Post
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from .models import Comment, Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
# from django.views.generic import *
from django.views.generic import *
# from django.contrib.auth.mixins import *
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

# class PostListView(LoginRequiredMixin, ListView):
#     model = Post
#     template_name = 'post/post_list.html'
#     context_object_name = 'posts'


# def register_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         confirm_password = request.POST.get("confirm_password")

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match")
#             return redirect("register_view")

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect("register_view")

#         User.objects.create_user(username=username, email=email, password=password)
#         messages.success(request, "Registration successful! Please log in.")
#         return redirect("login_view")  # Redirect to login page

#     return render(request, "user/register_view.html")

# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, 'post/post_list.html', {'posts': posts})

# def post_list(request):
#     posts = Post.objects.all().order_by('-created_at')

#     if request.method == 'POST':
#         post_id = request.POST.get('post_id')
#         author_username = request.POST.get('author')  # This is a string
#         content = request.POST.get('content')
#         post = get_object_or_404(Post, id=post_id)

#         if author_username and content:
#             # Convert username string to User instance
#             author = get_object_or_404(User, username=author_username)

#             # Create the comment
#             Comment.objects.create(post=post, author=author, content=content)
#             return redirect('post_list')

#     return render(request, 'post/post_list.html', {'posts': posts})

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        post = get_object_or_404(Post, id=post_id)

        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
            return redirect('post_list')

    return render(request, 'post/post_list.html', {'posts': posts})



def post_create(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST['category']
        tag_ids = request.POST.getlist('tags')
        image = request.FILES.get('image')
        print(image, 'img')

        category = Category.objects.get(id=category_id)
        post = Post.objects.create(
            title=title, content=content, image=image, category=category)

        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            post.tags.add(tag)
        return redirect('post_list')

    return render(request, 'post/post_create.html', {'categories': categories, 'tags': tags})

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)

    if request.user != post.user:
        return HttpResponseForbidden('You are not allowed to delete this post')
    post.delete()
    return redirect('post_list')



def update_post(request, id):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    post = get_object_or_404(Post, id=id)
    if request.user != post.user:
        return HttpResponse('You are not allowed to update this post')
    if request.method == "POST":
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.category = Category.objects.get(id=request.POST['category'])
        if 'image' in request.FILES:
            post.image = request.FILES['image']

        post.tags.clear()
        tag_ids = request.POST.getlist('tags')
        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            post.tags.add(tag)
        post.save()
        return redirect('post_list')
    return render(request, 'post/update_post.html', {'categories': categories, 'tags': tags, "post": post})


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register_view")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register_view")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration successful! Please log in.")
        return redirect("login")  # Redirect to login page

    return render(request, "user/register_view.html")


def login_view(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        # **credentials
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'login successfully  ')
            return redirect('post_list')
        else:
            messages.error(request, ' invalid credentials ')
            return redirect('post_list')

    return render(request, 'user/login.html', )


def logout_view(request):
    logout(request)
    messages.success(request, ' logout successfully ')
    return redirect('login_view')





def only(request, id):
    only = get_object_or_404(Post, id=id)
    return render(request, 'post/only.html', {'only': only})


