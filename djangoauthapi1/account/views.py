from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerilizer, UserLoginSerilizer, UserProfileSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

# Generate Token Mannually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serilizer = UserRegistrationSerilizer(data=request.data)
        if serilizer.is_valid(raise_exception=True):
            user = serilizer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration sucessful'},
                            status=status.HTTP_201_CREATED)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serilizer = UserLoginSerilizer(data=request.data)
        if serilizer.is_valid(raise_exception=True):
            email = serilizer.data.get('email')
            password = serilizer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
            

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serilizer = UserProfileSerializer(request.user)
        return Response(serilizer.data, status=status.HTTP_200_OK)
    
    #https://www.youtube.com/watch?v=lo7lBD9ynVc&t=9509s    1:51:23