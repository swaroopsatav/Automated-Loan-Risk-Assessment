from django.urls import path
from .views import (
    RegisterUserView, LoginView, UserProfileView,
    AdminUserDetailView, UserListView
)

app_name = "users"

urlpatterns = [
    path("auth/register/", RegisterUserView.as_view(), name="register"),  # Public-facing endpoint
    path("auth/login/", LoginView.as_view(), name="login"),  # Public-facing endpoint
    path("me/", UserProfileView.as_view(), name="profile"),  # Authenticated user profile
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="user-detail"),  # Admin-only detail view 
    path("admin/users/", UserListView.as_view(), name="user-list"),  # Admin-only list view
]
