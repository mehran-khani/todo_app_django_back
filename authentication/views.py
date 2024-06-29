from .models import User
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.user.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    def post(self, request):
        print(f"Incoming request data: {request.data}")  # Debugging line
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # user.generate_verification_token()
            user.send_verification_email()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response(
                {
                    "message": "User registered successfully. Please check your email for verification link.",
                    "user": UserSerializer(user).data,
                    "access": access_token,
                    "refresh": refresh_token,
                },
                status=status.HTTP_201_CREATED,
            )
        print(f"Errors: {serializer.errors}")  # Debugging line
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get("token")
        print(f"Received token: {token}")  # Debugging line

        try:
            users = User.objects.filter(verification_token=token)
            if not users.exists():
                print(f"No user found with token: {token}")  # Debugging line
                return Response(
                    {"detail": "Invalid verification token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for user in users:
                if default_token_generator.check_token(user, token):
                    user.is_active = True
                    user.verification_token = ""
                    user.save()
                    print(f"User {user.email} verified successfully!")  # Debugging line
                    return Response(
                        {"detail": "Email verified successfully!"},
                        status=status.HTTP_200_OK,
                    )

            print(f"Token {token} expired or invalid.")  # Debugging line
            return Response(
                {"detail": "Verification token expired or invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"Exception occurred: {str(e)}")  # Debugging line
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
