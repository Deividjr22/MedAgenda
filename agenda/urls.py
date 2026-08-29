from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("cadastro/", views.cadastro_view, name="cadastro"),
    path("medico/", views.medico_view, name="medico"),
    path("usuario/", views.usuario_view, name="usuario"),
    path("logout/", views.logout_view, name="logout"),
]
