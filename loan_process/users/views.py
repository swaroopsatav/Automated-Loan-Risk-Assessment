from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ValidationError
from loan_process.throttling import AuthRateThrottle, BurstRateThrottle, SensitiveEndpointThrottle
from .models import CustomUser
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserDetailSerializer,
    SecureUserSerializer,
    UserProfileSerializer,
)
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

logger = logging.getLogger(__name__)


# --- Registration View ---
class RegisterUserView(generics.CreateAPIView):
    """
    Handles user registration.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [BurstRateThrottle, AuthRateThrottle]

    def create(self, request, *args, **kwargs):
        # Call the parent's `create` method to perform the registration logic
        try:
            response = super().create(request, *args, **kwargs)
            # Add a success message
            response.data["message"] = "User registered successfully."
            return response
        except ValidationError as e:
            # If validation fails, return the validation errors directly
            if hasattr(e, 'detail') and isinstance(e.detail, dict) and 'password' in e.detail:
                # If it's a password validation error, return it directly
                return Response(
                    e.detail,
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # For other errors, keep the current format
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

# --- Login View (JWT-based) ---
class LoginView(APIView):
    """
    Handles user login and returns JWT tokens.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request):
        username = request.data.get("username", "").strip()
        email = request.data.get("email", "").strip()
        password = request.data.get("password", "").strip()


        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = authenticate(username=username,email=email,password=password)

            if not user:
                return Response(
                    {"error": "Invalid credentials. Please try again."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not user.is_active:
                return Response(
                    {"error": "User account is inactive. Please contact support."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": SecureUserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request):
        return Response(
            {"error": "Login is only available via POST."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

# --- Authenticated User Profile (GET, PUT) ---
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    GET: Fetch the authenticated user's profile.
    PUT/PATCH: Update the authenticated user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [SensitiveEndpointThrottle]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        try:
            # Restrict updates to specific fields
            restricted_fields = ["username", "email", "is_staff", "is_superuser", "is_active"]
            for field in restricted_fields:
                if field in request.data:
                    return Response(
                        {"error": f"You are not allowed to update the '{field}' field."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)

        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Update failed. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# --- Admin/User Detail View by ID ---
class AdminUserDetailView(generics.RetrieveAPIView):
    """
    Allows admin to fetch details of a specific user by ID.
    """
    queryset = CustomUser.objects.all()
    serializer_class = SecureUserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        try:
            return super().get_object()
        except Exception:
            raise NotFound(detail="User not found.")


# --- List Users (optional for admin) ---
class UserListView(generics.ListAPIView):
    """
    Allows admin to fetch the list of all users.
    """
    queryset = CustomUser.objects.all()
    serializer_class = SecureUserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = self.queryset.filter(is_active=True)

        # Add search functionality 
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(username__icontains=search)

        return queryset.order_by('username')


# --- Password Reset View ---
class PasswordResetView(APIView):
    """
    Handles password reset request by sending an email with a reset link.
    """
    permission_classes = [permissions.AllowAny]
    throttle_classes = [SensitiveEndpointThrottle]

    def post(self, request):
        email = request.data.get("email", "").strip()

        if not email:
            return Response(
                {"detail": "Email address is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # In a real implementation, you would check if the email exists,
            # generate a token, and send an email with a reset link
            # For this example, we'll just return a success response

            # Check if the email exists
            user_exists = CustomUser.objects.filter(email=email).exists()

            # Always return success to prevent email enumeration attacks
            return Response(
                {"detail": "Password reset link has been sent to your email address."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Password reset request error: {str(e)}")
            return Response(
                {"detail": "Unable to process your request. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# --- Password Reset Confirm View ---
class PasswordResetConfirmView(APIView):
    """
    Handles password reset using a token received via email.
    """
    permission_classes = [permissions.AllowAny]
    throttle_classes = [SensitiveEndpointThrottle]

    def post(self, request):
        token = request.data.get("token", "").strip()
        password = request.data.get("password", "").strip()

        if not token or not password:
            return Response(
                {"detail": "Token and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # In a real implementation, you would validate the token and find the user
            # For this example, we'll just return a success response
            # user = get_user_from_token(token)
            # user.set_password(password)
            # user.save()

            return Response(
                {"detail": "Password has been reset successfully."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            return Response(
                {"detail": "Unable to reset password. The link may be expired or invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# --- Password Change View ---
class PasswordChangeView(APIView):
    """
    Handles password change for authenticated users.
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [SensitiveEndpointThrottle]

    def post(self, request):
        current_password = request.data.get("current_password", "").strip()
        new_password = request.data.get("new_password", "").strip()

        if not current_password or not new_password:
            return Response(
                {"detail": "Current password and new password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user

        # Check if the current password is correct
        if not user.check_password(current_password):
            return Response(
                {"detail": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Validate the new password
            validate_password(new_password, user)

            # Set the new password
            user.set_password(new_password)
            user.save()

            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)

            return Response(
                {"detail": "Password has been changed successfully."},
                status=status.HTTP_200_OK,
            )
        except DjangoValidationError as e:
            return Response(
                {"detail": e.messages[0] if e.messages else "Password validation failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Password change error: {str(e)}")
            return Response(
                {"detail": "Unable to change password. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# --- OAuth Callback View ---
class OAuthCallbackView(APIView):
    """
    Handles OAuth callback from various providers.
    """
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, provider):
        code = request.data.get("code", "").strip()
        state = request.data.get("state", "").strip()

        if not code:
            return Response(
                {"detail": "Authorization code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # In a real implementation, you would exchange the code for tokens with the provider
            # and then authenticate or register the user
            # For this example, we'll just return a success response with mock tokens

            # Mock user authentication
            user = CustomUser.objects.first()  # Just for demonstration
            if not user:
                return Response(
                    {"detail": "Authentication failed."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Generate tokens
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": SecureUserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"OAuth callback error: {str(e)}")
            return Response(
                {"detail": f"Unable to complete {provider} authentication. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
