from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("cadastro/", views.cadastro_view, name="cadastro"),
    path("usuario/", views.cadastrar_agendamento, name="cadastrar_agendamento"),
    path(
        "usuario/", views.cadastrar_agendamento, name="usuario"
    ),  # Alias para compatibilidade com os templates
    path("medico/", views.pagina_medico, name="pagina_medico"),
    path("logout/", views.logout_view, name="logout"),
]
