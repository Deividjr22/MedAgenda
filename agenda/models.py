from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Medico(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)
    crm = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Dr(a). {self.nome} - {self.especialidade}"


class Agendamento(models.Model):
    paciente = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="agendamentos"
    )
    medico = models.ForeignKey(
        Medico, on_delete=models.CASCADE, related_name="agendamentos"
    )
    data = models.DateField()
    horario = models.TimeField()
    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta: {self.paciente.username} com {self.medico.nome} em {self.data} às {self.horario}"
