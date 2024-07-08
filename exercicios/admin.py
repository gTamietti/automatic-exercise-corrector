from django.contrib import admin
from .models import Exercicio, Codigo

admin.site.register(Exercicio)

@admin.register(Codigo)
class CodigoAdmin(admin.ModelAdmin):
    list_display = ('exercicio', 'date_submition', 'result')  
    list_filter = ('exercicio', 'date_submition') 
    search_fields = ('exercicio',)  