from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_exercicios, name='lista_exercicios'),
    path('exercicio/<int:exercicio_id>/', views.detalhe_exercicio, name='detalhe_exercicio'),
    path('submission_result/<int:submission_id>', views.submission_result, name= 'submission_result'),
]
