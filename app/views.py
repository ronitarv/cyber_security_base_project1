from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.db import connection
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import Post
from .forms import LoginForm, UserCreationForm

import string
import random


@login_required
@csrf_protect
def home(request):
    posts = Post.objects.all().filter(Q(is_public=True) | Q(publisher=request.user))
    titles = [x.title for x in posts]
    post_content = ""
    if ("post_content" in request.session):
        post_content = request.session["post_content"]

    return render(request, "app/home.html", {"titles": titles, "post_content": post_content})

@login_required
@csrf_protect
def post(request):
    if request.method == "POST":
        titles = [x.title for x in (Post.objects.all())]
        if (request.POST.get("title") not in titles and request.POST.get("title") != "" and request.POST.get("content") != ""):
            is_public = False
            if ("is_public" in request.POST):
                is_public = True
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO app_post (publisher_id, title, content, is_public) VALUES ({request.user.id}, '{request.POST.get('title')}', '{request.POST.get('content')}', {is_public})")
            # post = Post(publisher = request.user, title = request.POST.get("title"), content = request.POST.get("content"), is_public=is_public)
            # post.save()
    return redirect("/")

@login_required
@csrf_protect
def open(request):
    post = Post.objects.get(title=request.GET.get("selected_post"))
    request.session["post_content"] = post.content

    return redirect("/")

@csrf_protect
def verify(request):
    request.session["tfa_token"] = "".join(random.choice(string.ascii_lowercase) for i in range(8))
    return redirect('/verify-wait')

@csrf_protect
def verify_wait(request):
    return render(request, 'app/verify_wait.html', {"not_in_real_app_give_token": request.session["tfa_token"]})

@csrf_protect
def verify_confirm(request):
    if (request.method == "POST" and "user_pk" in request.session and 
        "tfa_token" in request.session and request.session["tfa_token"] == request.POST.get("tfa_token")):
        user = User.objects.get(pk=request.session["user_pk"])
        if user:
            login(request, user)
    return redirect("/")

@csrf_protect
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            #try:
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                request.session["user_pk"] = user.pk
                return redirect('/verify')
            # except LockedOut:
            #     messages.warning(request, "Account has been locked out for too many failed login attempts")
            # elif "try_count" not in request.session:
            #     request.session["try_count"] = 1
            # else:
            #     request.session["try_count"] += 1
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})

@csrf_protect
def user_logout(request):
    logout(request)
    return redirect('/')

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# FOR DEBUGGING ------------------------------------------------
@csrf_protect
def delete(request):
    Post.objects.all().delete()
    return redirect("/")