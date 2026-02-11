from rest_framework.generics import GenericAPIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from apps.account.serializers import AuthTokenSerializer


class Login(GenericAPIView):
    serializer_class = AuthTokenSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "role": user.is_superuser,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )