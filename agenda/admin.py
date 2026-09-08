from django.contrib import admin
from .models import Medico, Agendamento


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ("user", "especialidade", "crm", "telefone")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "crm",
        "especialidade",
    )


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ("paciente", "medico", "data", "horario", "criado_em")
    list_filter = ("data", "medico")
    search_fields = ("paciente__username", "medico__user__username", "medico__crm")
