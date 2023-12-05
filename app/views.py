from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Post


@login_required
@csrf_protect
def home(request):
    return render(request, "app/home.html")

@login_required
@csrf_protect
def post(request):
    is_public = False
    if (hasattr(request.POST, "is_public")):
        is_public = True
    post = Post(publisher = request.user, content = request.POST["message"], is_public=is_public)
    post.save()
    return redirect("/")