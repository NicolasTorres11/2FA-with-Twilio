from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from codes.models import CustomUser
from .utils import send_sms


class HomeView(APIView):
    @login_required
    def get(self, request):
        return Response({'message': 'Welcome to the main page'})


class AuthView(APIView):
    def get(self, request):
        return Response({
            'page': 'login',
            'submit_value': 'Ingresar'
        })

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pk'] = user.pk
            return Response({
                'messages': 'Youre Login'
            })
        else:
            messages.error(request, 'el usuario o la contraseña son incorrectas')
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home_view')

        return Response({
            'page': 'register',
            'submit_value': 'Registrarse'
        })

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = CustomUser(username=username.lower())
        user.set_password(password)
        user.save()
        return redirect('home_view')


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('index')


class VerifyView(APIView):
    def get(self, request):
        pk = request.session.get('pk')
        if pk:
            user = CustomUser.objects.get(pk=pk)
            code = user.codes
            code_user = f'{user.username}: {user.codes}'
            if not request.data:
                send_sms(code_user, user.phone_number)
            return Response({})
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        pk = request.session.get('pk')
        if pk:
            user = CustomUser.objects.get(pk=pk)
            code = user.codes
            num = request.data.get('number')
            if str(code) == num:
                code.save()
                login(request, user)
                return redirect('home_view')
            else:
                return redirect('login')
        return Response(status=status.HTTP_400_BAD_REQUEST)