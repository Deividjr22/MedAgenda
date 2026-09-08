from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="medico")
    especialidade = models.CharField(max_length=100)
    crm = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        nome_completo = self.user.get_full_name() or self.user.username
        return f"Dr(a). {nome_completo} - {self.especialidade}"


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ("Agendado", "Agendado"),
        ("Concluido", "Concluído"),
        ("Cancelado", "Cancelado"),
    ]

    paciente = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="agendamentos"
    )
    medico = models.ForeignKey(
        Medico, on_delete=models.CASCADE, related_name="agendamentos"
    )
    data = models.DateField()
    horario = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Agendado")
    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        nome_medico = self.medico.user.get_full_name() or self.medico.user.username
        return f"Consulta: {self.paciente.username} com Dr(a). {nome_medico} em {self.data} às {self.horario}"
