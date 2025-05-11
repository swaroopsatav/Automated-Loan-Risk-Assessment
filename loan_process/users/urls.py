
from django.urls import path
from .views import (
    RegisterUserView, LoginView, UserProfileView,
    AdminUserDetailView, UserListView,
    PasswordResetView, PasswordResetConfirmView, 
    PasswordChangeView, OAuthCallbackView
)

app_name = "users"

urlpatterns = [
    # Public-facing endpoints
    path("auth/register/", RegisterUserView.as_view(), name="register"),
    path("", LoginView.as_view(), name="login"),
    path("api/users/auth/login/", LoginView.as_view(), name="api-login"),  # Added to match frontend expectation

    # Password management
    path("api/users/auth/password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path("api/users/auth/password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("api/users/auth/password-change/", PasswordChangeView.as_view(), name="password-change"),

    # OAuth callback
    path("api/users/auth/<str:provider>/callback/", OAuthCallbackView.as_view(), name="oauth-callback"),

    # Authenticated user profile
    path("me/", UserProfileView.as_view(), name="profile"),

    # Admin-only endpoints
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="user-detail"),
    path("admin/users/", UserListView.as_view(), name="user-list"),
]
