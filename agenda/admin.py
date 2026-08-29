from django.contrib import admin
from .models import Medico, Agendamento


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "especialidade", "crm", "telefone")
    search_fields = ("nome", "crm", "especialidade")


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ("paciente", "medico", "data", "horario", "criado_em")
    list_filter = ("data", "medico")
    search_fields = ("paciente__username", "medico__nome")
