from django.urls import path, include, re_path
from allauth.account import views
from . import views as my_views

urlpatterns = [
    path("signup/", my_views.MySignupView.as_view(),name="account_signup"),
    path("login/", my_views.MyLoginView.as_view(),name="account_login"),
    path("logout/", views.logout, name="account_logout"),
    path("password/change/", views.password_change,name="account_change_password"),
    path("password/set/", views.password_set, name="account_set_password"),
    path("inactive/", views.account_inactive, name="account_inactive"),
    
    # E-mail
    path("email/", views.email, name="account_email"),
    path("confirm-email/", views.email_verification_sent,name="account_email_verification_sent"),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", my_views.MyConfirmEmailView.as_view(),name="account_confirm_email"),

    # password reset
     path("password/reset/", my_views.MyPasswordResetView.as_view(),
         name="account_reset_password"),
    path("password/reset/done/", views.password_reset_done,
         name="account_reset_password_done"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
            views.password_reset_from_key,
            name="account_reset_password_from_key"),
    path("password/reset/key/done/", views.password_reset_from_key_done,
         name="account_reset_password_from_key_done"),
]
