from django.shortcuts import get_object_or_404, render
from rest_framework import generics,status
from rest_framework.response import Response
from follow.models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from follow.utils import send_verification_code
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema



class UserRegister(generics.CreateAPIView):
    serializer_class = UserRegisterSerializers

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        user = self.request.data.get('email')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # self.perform_create(serializer)
        send_verification_code(user)
        return Response("Код был отправлен на ваш email")

 

class UserCodeView(generics.UpdateAPIView):
    serializer_class = UserCodeSerializers

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            
     

            user = CustomUser.objects.get(code=code)
            refresh = RefreshToken.for_user(user=request.user)

            if code == user.code:
                return Response({'detail': 'Successfully confirmed your code',
                                'refresh-token':str(refresh),
                                'access': str(refresh.access_token),
                                'refresh_lifetime_days': refresh.lifetime.days,
                                'access_lifetime_days': refresh.access_token.lifetime.days

                                })
            
            else:
                return Response({'status': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors)
            

class UserSendCodeView(generics.CreateAPIView):
    serializer_class = UserSendCodeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        send_verification_code(email=email)
        return Response("Код был отправлен на ваш email")
    

class CheckCodeView(generics.UpdateAPIView):
    serializer_class = UserCodeSerializers

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializers = self.get_serializer(data = request.data)

        if serializers.is_valid():
            code = serializers.validated_data['code']
            if code == user.code:
                return Response("The code accepted", status=status.HTTP_200_OK)
            else:
                return Response("The code is valid", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializers.errors)

class UserRessetPasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if check_password(old_password, request.user.password):
            user.set_password(new_password)
            user.save()
            return Response({"detail":"the password successfully updated"},status=status.HTTP_201_CREATED)
        else:
            return Response("The password does not match")