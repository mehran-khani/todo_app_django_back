from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.settings import api_settings as jwt_setting
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from api import exceptions
from api.auth.token.serializers import TokenCreateSerializer, TokenRefreshSerializer
from api.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed


class TokenCreateView(jwt_views.TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = TokenCreateSerializer

    def post(self, request: jwt_views.Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request=request,
            username=serializer.validated_data.get("email"),
            password=serializer.validated_data.get("password"),
        )

        if not user:
            raise AuthenticationFailed(
                {
                    "detail": "No active account found with the given credentials",
                    "code": "no_active_account",
                }
            )

        try:
            refresh = RefreshToken.for_user(user)
        except TokenError:
            raise exceptions.BadRequest(
                {"detail": "Invalid Token", "code": "invalid_token"}
            )

        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status.HTTP_200_OK,
        )


class TokenRefreshView(jwt_views.TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer
