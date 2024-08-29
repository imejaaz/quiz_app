from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class SignUpView(APIView):
    def post(self, request):
        f_name = request.data.get('first_name')
        l_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([f_name, l_name, email, password]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            first_name=f_name,
            last_name=l_name,
            email=email,
            username=email,
            password=password
        )
        if request.user.is_superuser:
            user.is_staff = True
        user.save()

        return Response({
            "success": "User created successfully.",
        }, status=status.HTTP_201_CREATED)


class UserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([email, password]):
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            if user.is_superuser:
                role = "superuser"
            elif user.is_staff:
                role = "admin"
            else:
                role = "user"
            return Response({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "token": token.key,
                "role": role,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):

        if not request.user.is_authenticated:
            raise PermissionDenied(
                "You do not have permission to access this resource.")

        if not request.user.is_staff:
            return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.filter(
            is_active=True, is_staff=False, is_superuser=False)
        user_data = [
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
            for user in users
        ]

        return Response({"users": user_data}, status=status.HTTP_200_OK)
