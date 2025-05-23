from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import EmailAuthenticationForm

app_name = "users"

urlpatterns = [
    path("home/", views.home_view, name="home"),
    path("register/", views.register_view, name="register"),
    path("confirm/<str:code>/", views.confirm_email, name="confirm_email"),
    path(
        "login/",
        LoginView.as_view(
            template_name="users/login.html",
            authentication_form=EmailAuthenticationForm,
            redirect_authenticated_user=True,  # если пользователь уже вошёл — сразу редиректим
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
]
