from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medico, Agendamento


def login_view(request):
    if request.method == "POST":
        pass
    return render(request, "agenda/Login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def cadastro_view(request):
    if request.method == "POST":
        pass
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
