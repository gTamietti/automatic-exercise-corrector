from django.shortcuts import render, get_object_or_404, redirect
from .models import Exercicio, Codigo
from .forms import FormCode
import subprocess

# request é usado para processar a requisição HTTP e redenizar o template

def lista_exercicios(request):
    # A funcao 'Exercicio.objects.all()' retorna todos os exercicios do banco do tipo 'Exercicio'
    exercicios = Exercicio.objects.all()
    return render(request, 'exercicios/lista_exercicios.html', {'exercicios': exercicios})


def detalhe_exercicio(request, exercicio_id):
    exercicio = get_object_or_404(Exercicio, pk=exercicio_id)
    if request.method == 'POST':
        form = FormCode(request.POST, request.FILES)
        submission = form.save(commit=False)
        submission.exercicio = exercicio
        submission.save()

        try:
            result = subprocess.run(
                ['python3', submission.code_file.path],
                input=exercicio.pubin,
                capture_output=True,
                text=True
            )
            output = result.stdout.strip()
            expected_output = exercicio.pubout.strip()
            if output == expected_output:
                submission.result = 'Exercício Correto'
            else:
                submission.result = 'Exercício Incorreto'
            submission.save()

            return redirect('submission_result', submission_id=submission.id)
        
        except Exception as e:
            submission.result = 'Erro na execuçâo'
            submission.save()
            print(f'Erro na execução: {str(e)}') 
            output = str(e)

    else:
        form = FormCode()
    return render(request, 'exercicios/detalhe_exercicio.html', {'exercicio': exercicio, 'form': form})


def submission_result(request, submission_id):
    submission = get_object_or_404(Codigo, pk=submission_id)
    return render(request, 'exercicios/submission_result.html', {'submission': submission})
