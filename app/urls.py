from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("signup/", views.user_signup, name="signup"),
    path("verify/", views.verify, name="verify"),
    path("verify-wait/", views.verify_wait, name="verify-wait"),
    path("verify-confirm/", views.verify_confirm, name="verify-confirm"),
    path("post/", views.post, name="post"),
    path("open/", views.open, name="open"),
    path("delete/", views.delete, name="delete"), # DEBUGGING!!!!
]