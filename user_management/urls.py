from django.urls import path
from . import views

app_name = "user_management"

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("change_password", views.change_password, name="change_password"),
    path("forget_password", views.forget_password, name="forget_password"),
    path("reset_password/<str:reset_code>", views.reset_forgotten_password, name="reset_password"),
    path("account_settings", views.account_settings, name="account_settings"),
    path("email_conformation/<str:email_code>", views.confirm_email, name="confirm_email")
]
