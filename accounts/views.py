from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import UserRegisterSerializer, UserLoginSerializer, RefreshTokenSerializer
from accounts.utils import get_tokens_for_user
from shared.utils.custom_response import CustomResponse


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                message_key='SUCCESS',
                data=serializer.data,
                request=request,
                name='mahmud'
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            return CustomResponse.success(
                message_key='SUCCESS',
                data=tokens,
                request=request
            )
        else:
            return CustomResponse.error(
                message_key='ERROR',
                data=serializer.errors,
                request=request
            )


class GetAccessToken(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh_token']

        if refresh_token is None:
            return CustomResponse.error(
                message_key='ERROR',
                data={'detail': 'refresh_token is invalid'},
                request=request
            )
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return CustomResponse.success(
            message_key='SUCCESS',
            data={'access_token': access_token},
            request=request
        )

class UserIsAuthenticated(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return CustomResponse.success(
                message_key='SUCCESS',
                data={'message': 'isAuthenticated', 'user': request.user.username},
                request=request
            )
        else:
            return CustomResponse.error(
                message_key='ERROR',
                request=request
            )
