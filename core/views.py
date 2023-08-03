from django.shortcuts import render, redirect
from .models import Pessoa

# Ler pessoas do banco
def home(request):
# Dentro da várivel pessoas tenho todas as pessoas que estão no banco de dados
    pessoas = Pessoa.objects.all()
    return render(request, "index.html", {"pessoas": pessoas})

# Salvar pessoas cadastradas
def salvar(request):
    vnome = request.POST.get("nome")
    Pessoa.objects.create(nome=vnome)
    pessoas = Pessoa.objects.all()
    return render(request, "index.html", {"pessoas": pessoas})

# Editar pessoas cadastradas
def editar(request, id):
    pessoa = Pessoa.objects.get(id=id)
    return render(request, "update.html", {"pessoa": pessoa})

# Atualizar pessoas cadastradas
def update(request, id):
    vnome = request.POST.get("nome")
    pessoa = Pessoa.objects.get(id=id)
    pessoa.nome = vnome
    pessoa.save()
    return redirect(home)

# Deletar pessoas cadastradas
def delete(request, id):
   pessoa = Pessoa.objects.get(id=id)
   pessoa.delete()
   return redirect(home)