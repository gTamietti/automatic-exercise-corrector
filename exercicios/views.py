from django.shortcuts import render, get_object_or_404, redirect
from .models import Exercicio, Codigo
from .forms import FormCode
import subprocess
import os

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

        code_file_path = submission.code_file.path
        file_extension = os.path.splitext(code_file_path)[1]
        class_name = os.path.splitext(os.path.basename(code_file_path))[0]
        java_class_dir = os.path.dirname(code_file_path)

        try:
            if file_extension == '.py':
                result = subprocess.run(
                    ['python3', code_file_path],
                    input=exercicio.pubin,
                    capture_output=True,
                    text=True
                )
            elif file_extension == '.java':
                compile_result = subprocess.run(
                    ['javac', code_file_path],
                    capture_output=True,
                    text=True
                )
                if compile_result.returncode == 0:
                    result = subprocess.run(
                        ['java',class_name],
                        cwd=java_class_dir,
                        input=exercicio.pubin,
                        capture_output=True,
                        text=True
                )
                else:
                    raise Exception(f'Erro na compilação: {compile_result.stderr}')
            else:
                raise Exception('Formato de arquivo não suportado')

            output = result.stdout.strip()
            expected_output = exercicio.pubout.strip()
            if output == expected_output:
                submission.result = 'Exercício Correto'
            else:
                submission.result = 'Exercício Incorreto'
            submission.save()
            os.remove(code_file_path)
            return redirect('submission_result', submission_id=submission.id)

        except Exception as e:
            submission.result = 'Erro na execução'
            submission.save()
            print(f'Erro na execução: {str(e)}')
            output = str(e)

    else:
        form = FormCode()
    return render(request, 'exercicios/detalhe_exercicio.html', {'exercicio': exercicio, 'form': form})

def submission_result(request, submission_id):
    submission = get_object_or_404(Codigo, pk=submission_id)
    return render(request, 'exercicios/submission_result.html', {'submission': submission})
