from django.http import response
from django.http.response import HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from api.models import CustomUser, Post
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
from django.core.mail import EmailMessage
import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .email_token_generator import email_verify_token
from django.urls import reverse

from api.models import Post 

class RegisterView(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            current_site = get_current_site(request)
            email_subject = 'Verify Your Email'
            link = reverse('verify', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(serializer.data['username'])), 'token': email_verify_token.make_token(serializer.data)})
            message = 'http://'+current_site.domain+link
            email_to = serializer.data['email']
            email = EmailMessage(email_subject, message, to=[email_to])
            email.send(fail_silently=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = jwt.encode({'username': user.username}, settings.JWT_SECRET_KEY, algorithm='HS256')

            serializer = RegisterSerializer(user)

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def verify_email(request, uidb64, token):
    try:
        username = force_bytes(urlsafe_base64_decode(uidb64)).decode()
        user = CustomUser.objects.filter(username=username).first()
        userData = UserSerializer(CustomUser.objects.filter(username=username).first()).data
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and email_verify_token.check_token(userData, token):
        user.is_verified = True
        user.save()
        return HttpResponse('Your account has been activated successfully')
    else:
        return HttpResponse('Activation link is invalid!')

# class postLists(APIView):
#     def get(self, request):
#         manyPosts = Post.objects.all()
#         serializer = PostSerializer(manyPosts, many = True)
#         return response(serializer.data)