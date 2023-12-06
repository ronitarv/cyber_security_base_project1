from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.db import connection
from .models import Post


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

def open(request):
    post = Post.objects.get(title=request.GET.get("selected_post"))
    request.session["post_content"] = post.content
    return redirect("/")


# FOR DEBUGGING ------------------------------------------------
@csrf_protect
def delete(request):
    Post.objects.all().delete()
    return redirect("/")