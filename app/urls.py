from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/", views.post, name="post"),
    path("open/", views.open, name="open"),
    path("delete/", views.delete, name="delete") # DEBUGGING!!!!
]