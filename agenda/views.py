from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path
from . import views

def home(request):
    return HttpResponse("Olá! Esta é a página inicial.")

def pagina_usuario(request):
    contexto = {'nome': 'Juliana'}
    return render(request, 'Usuario.html', contexto)


class CustomLoginView(LoginView):
    template_name = "login.html"

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "cadastro.html"
    success_url = reverse_lazy("login")

    