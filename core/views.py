from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from codes.forms import CodeForm
from app.models import CustomUser
from .utils import send_sms
from django.contrib import messages


@login_required
def home_view(request):
    return render(request, 'main.html', {})


def auth_view(request):
    form = UserLoginForm
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pk'] = user.pk
            return redirect('verify_view')
        else:
            messages.error(request, 'el usuario o la contraseña son incorrectas')
    return render(request, 'auth.html', {
        'form': form,
        'page': 'login',
        'submit_value': 'Ingresar'
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home_view')

    form = UserRegisterForm
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('home_view')
        else:
            messages.error(request, 'Ocurrio un Error Durante el registro')

    return render(request, 'auth.html', {
        'form': form,
        'page': 'register',
        'submit_value': 'Registrarse'
    })


def logout_view(request):
   logout(request)
   return redirect('index')


def verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = CustomUser.objects.get(pk=pk)
        code = user.codes
        code_user = f'{user.username}: {user.codes}'
        if not request.POST:
            send_sms(code_user, user.phone_number)
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(code) == num:
                code.save()
                login(request, user)
                return redirect('home_view')
            else:
                return redirect('login')
    return render(request, 'verify.html', {'form': form})
