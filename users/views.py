from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AuthenticationUser
from .serializers import AuthenticationUserSerializer, TokenSerializer
from services.authorizer import AuthorizationService
from rest_framework.permissions import IsAuthenticated


class TestListCreateAPIView(APIView):
    serializer_class = AuthenticationUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        auth_service = AuthorizationService()
        access_token = auth_service.generate_access_token(user.username)
        refresh_token = auth_service.generate_refresh_token(user.username)

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token
        })


class TestRetrieveUpdateDestroyAPIView(APIView):
    serializer_class = AuthenticationUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(AuthenticationUser, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=204)


class RefreshTokenView(APIView):
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthorizationService()
        try:
            username = auth_service.decode_token(serializer.validated_data['refresh_token'])
            auth_service.validate_token(serializer.validated_data['refresh_token'], username)
        except Exception as e:
            return Response({'error': str(e)}, status=401)

        access_token = auth_service.generate_access_token(username)
        return Response({'access_token': access_token})