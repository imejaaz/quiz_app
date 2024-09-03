from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.user.role)

        if request.user.role == 'user':
            return Response({"error": "You have not permissions to access it."}, status=status.HTTP_400_BAD_REQUEST)
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
            role='user',
            password=password,
            created_by=request.user
        )
        if request.user.is_superuser:
            user.is_staff = True
            user.role = 'admin'
        user.save()
        return Response({
            "success": "User created successfully.",
        }, status=status.HTTP_201_CREATED)


class UserView(APIView):
    # sign in
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
            elif user.role == 'admin':
                role = "admin"
            else:
                role = "user"
            return Response({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "token": token.key,
                "country": user.country,
                "role": role,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):

        if not request.user.is_authenticated:
            raise PermissionDenied(
                "You are not authenticated.")

        if request.user.role == "user":
            return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.filter(
            is_active=True, is_staff=False, is_superuser=False)
        user_data = [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
            for user in users
        ]

        return Response({"users": user_data}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user.role == 'user':
            return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, id=pk)
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateProfileView(request):
    user = request.user
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    country = request.data.get('country')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if country is not None:
        user.country = country
        user.save()

    if old_password and new_password:
        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        if len(new_password) < 8:
            return Response({"error": "New password must be at least 8 characters long."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        update_session_auth_hash(request, user)

    user.save()

    return Response({"success": "Profile updated successfully."}, status=status.HTTP_200_OK)
