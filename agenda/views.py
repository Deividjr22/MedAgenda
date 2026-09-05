import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Medico, Agendamento, Perfil


def login_view(request):
    if request.method == "POST":
        identificador = request.POST.get("username")
        password = request.POST.get("password")

        username = identificador

        # Se digitaram um e-mail, busca o username correspondente no banco
        if "@" in identificador:
            try:
                user_obj = User.objects.get(email=identificador)
                username = user_obj.username
            except User.DoesNotExist:
                username = None

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("usuario")
        else:
            messages.error(request, "Usuário, e-mail ou senha inválidos.")
            return redirect("login")

    return render(request, "agenda/Login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def cadastro_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        telefone_bruto = request.POST.get("telefone", "")
        cpf_bruto = request.POST.get("cpf", "")

        if password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return redirect("cadastro")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nome de usuário já está em uso.")
            return redirect("cadastro")

        tel_limpo = re.sub(r"\D", "", telefone_bruto)
        cpf_limpo = re.sub(r"\D", "", cpf_bruto)

        telefone = (
            f"({tel_limpo[:2]}) {tel_limpo[2:7]}-{tel_limpo[7:]}"
            if len(tel_limpo) == 11
            else (
                f"({tel_limpo[:2]}) {tel_limpo[2:6]}-{tel_limpo[6:]}"
                if len(tel_limpo) == 10
                else telefone_bruto
            )
        )
        cpf = (
            f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
            if len(cpf_limpo) == 11
            else cpf_bruto
        )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        Perfil.objects.create(user=user, telefone=telefone, cpf=cpf)

        messages.success(request, "Cadastro realizado com sucesso! Faça login.")
        return redirect("login")
    return render(request, "agenda/Cadastro.html")


def medico_view(request):
    return render(request, "agenda/Medico.html")


@login_required
def usuario_view(request):
    if request.method == "POST":
        medico_id = request.POST.get("medico")
        data = request.POST.get("data")
        horario = request.POST.get("horario")
        observacao = request.POST.get("observacao", "")

        if not medico_id or not data or not horario:
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")
        else:
            try:
                medico = Medico.objects.get(id=medico_id)
                Agendamento.objects.create(
                    paciente=request.user,
                    medico=medico,
                    data=data,
                    horario=horario,
                    observacao=observacao,
                )
                messages.success(request, "Consulta agendada com sucesso!")
                return redirect("usuario")
            except Medico.DoesNotExist:
                messages.error(request, "Médico selecionado não encontrado.")

    medicos = Medico.objects.all()
    meus_agendamentos = Agendamento.objects.filter(paciente=request.user).order_by(
        "data", "horario"
    )
    context = {"medicos": medicos, "agendamentos": meus_agendamentos}
    return render(request, "agenda/Usuario.html", context)
