from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Agendamento, Medico


def login_view(request):
    if request.method == "POST":
        username_input = request.POST.get("username")
        password_input = request.POST.get("password")

        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            login(request, user)

            # Redireciona o Médico para o painel dele e o Paciente para a tela dele
            if hasattr(user, "medico"):
                return redirect("pagina_medico")
            return redirect("cadastrar_agendamento")
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "agenda/login.html")


@login_required
def cadastrar_agendamento(request):
    if request.method == "POST":
        medico_id = request.POST.get("medico")
        data = request.POST.get("data")
        horario = request.POST.get("horario")
        observacao = request.POST.get("observacao")

        medico = Medico.objects.get(id=medico_id)

        Agendamento.objects.create(
            paciente=request.user,
            medico=medico,
            data=data,
            horario=horario,
            observacao=observacao,
            status="Agendado",
        )
        messages.success(request, "Consulta agendada com sucesso!")
        return redirect("cadastrar_agendamento")

    medicos = Medico.objects.all()
    agendamentos = Agendamento.objects.filter(paciente=request.user).order_by(
        "data", "horario"
    )

    return render(
        request,
        "agenda/Usuario.html",
        {"medicos": medicos, "agendamentos": agendamentos},
    )


@login_required
def pagina_medico(request):
    if hasattr(request.user, "medico"):
        agendamentos = Agendamento.objects.filter(medico=request.user.medico).order_by(
            "data", "horario"
        )
    else:
        agendamentos = Agendamento.objects.all().order_by("data", "horario")

    return render(request, "agenda/Medico.html", {"agendamentos": agendamentos})


def cadastro_view(request):
    if request.method == "POST":
        # Adicione aqui a lógica de cadastro se houver
        pass
    return render(request, "agenda/Cadastro.html")


def logout_view(request):
    logout(request)
    return redirect("login")
