from django.db import models

# Criação do banco de dados da parte de exercicio com entrada e saida

class Exercicio(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    pubin = models.TextField(verbose_name='Input')
    pubout = models.TextField(verbose_name='Saida esperada')

    def __str__(self):
        return self.title
    
#  Parte que recebe o codigo com chave estrangeira de exercicio com modelo
# Cascade para remoção de todos os dados de Codigo caso o exercicio referente
# seja deletado

class Codigo(models.Model):
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    code_file = models.FileField(upload_to='code_submissions/')
    date_submition = models.DateTimeField(auto_now_add=True)
    result = models.TextField(blank=True, null=True)

# Modelo de representaçao mais legível para saber qual exercicio foi enviado

    def __str__(self):
        return f'{self.exercicio.title} enviado'