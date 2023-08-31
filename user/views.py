from django.shortcuts import render
from .serializers import RegistrationSerializer, LoginSerializer,UserSerializer, ProfileSerializer,AdminRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Profile

# Create your views here.

class AdminRegistrationView(APIView):
    serializer_class = AdminRegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            admin = serializer.save()
            refresh = RefreshToken.for_user(admin)

            responce_data = {
                'success':'Admin registerd sucessfully..',
                'admin': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }

            return Response(responce_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            responce_data = {
                'success':'User registerd sucessfully..',
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }

            return Response(responce_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'Logout successful.'}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)



class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    
class UserProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        user_profile, created = Profile.objects.get_or_create(user=self.request.user)
        user_profile.email = user.email
        user_profile.full_name = user.first_name+' '+user.last_name
        return user_profile