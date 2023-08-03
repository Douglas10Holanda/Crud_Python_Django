"""
### Criação do Projeto ###

# Cria um ambiente virtual para cada cliente
    python -m venv cliente1

# Ativar venv
    cd cliente1
    cd Scripts
    activate
    cd ..
    cd ..

# Instalar django
    pip install django

# Criar projeto django
    django-admin startproject app .

# Rodar projeto django
    python manage.py runserver

# Cria um banco de dados com estruturas básicas
    python manage.py migrate

# Criar um super usuário
    python manage.py createsuperuser


### CRUD ###

# Criar partes do sistemas(apps)
    python manage.py startapp core

# Registrar app no settings em "installed apps"
    'core'

# Criar URL nova
    adicionar include ("from django.urls import path, include")
    adicionar url em url patterns ("path('core/', include('core.urls'))")
    adicionar arquivo urls.py em core e copiar e colar código
    adicionar as views ("from .views import home")
    criar função 'home' em view.py (    def home(request):
                                            return render(request, "index.html")
    )
    modificar urls.py de core para ("path('', home)")
    dentro da pasta core, criar uma pasta 'templates'
    dentro da pasta templates, criar um aquivo chamado 'index.html'


### 1º PARTE DO CRUD ---- LEITURA (Read) ###

    Em models.py na pasta core, crie uma class Pessoa (     class Pessoa(models.Model):
                                                                nome = models.CharField(max_length=100)
    )
    Depois que criar o model, devo registrar esse model em admin.py (       from .models import Pessoa
                                                                            admin.site.register(Pessoa)
    )

# Criar migrations
    python manage.py makemigrations
    dentro da pasta migrations em core, ele cria um arquivo chamado '0001_initial.py' com informações de como a tabela deve ser criada
    python manage.py migrate
    depois de rodar 'python manage.py migrate' a tabela foi criada no banco

# Agora posso cadastrar pessoas no banco de dados pela interface do django
    para a visualização do nome ficar correta e não mostrar 'pessoa_object' devo adicionar (    def __str__(self):
                                                                                                    return self.nome
    ) em models.py no model pessoa

## (R)EAD ##
    Devo importar o model para view.py (    from .models import Pessoa)
    Em seguida pego todas a pessoa do banco de dados (      def home(request):
                                                                pessoas = Pessoa.objects.all()
                                                                return render(request, "index.html")
    )
    Depois eu envio ela para o meu template(                def home(request):
                                                                pessoas = Pessoa.objects.all()
                                                                return render(request, "index.html", {"pessoas": pessoas})
    )
    Agora dentro do meu template, tenho acesso as pessoas do banco

    # Imprimir as pessoas na tela
        adiciono o código no arquivo index.html(        
            <ul>
                {% for pessoa in pessoas %}
                    <li>{{ pessoa.id }}, {{ pessoa.nome }}</li>
                {% endfor %}
            </ul>
        )

## (C)REATE ##
    Devo criar um form action
    Devo criar um input 
    Devo criar um button
    # Adicionar a url salvar no form action (
        <form action="{% url 'salvar' %}">
            <input type="text" name="nome">
            <button type="submit">Salvar</button>
        </form>
    )
    # Devo criar a url salvar em urls.py na pasta core e importar a view salvar (      
            from django.contrib import admin
            from django.urls import path, include
            from .views import home, salvar
            
            urlpatterns = [
                path('', home)
                path('salvar/', salvar, name="salvar")
            ]
    ) 

    # Criar view salvar (
        def salvar(request):
            vnome = request.POST.get("nome")
            Pessoa.objects.create(nome=vnome)
            pessoas = Pessoa.objects.all()
            return render(request, "index.html", {"pessoas": pessoas})
    )
    Adicionar method POST no form action (
        <form action="{% url 'salvar' %}" method="POST">
            <input type="text" name="nome">
            <button type="submit">Salvar</button>
        </form>
    )
    Adicionar proteção csrf token no arquivo index.html(
        <form action="{% url 'salvar' %}" method="POST">
            {% csrf_token %}
            <input type="text" name="nome">
            <button type="submit">Salvar</button>
        </form>
    )

### (U)pdate ###
    # Devo adicionar um link na lista de pessoas para editar suas informações(
        <ul>
            {% for pessoa in pessoas %}
                <li>{{ pessoa.id }}, {{ pessoa.nome }} <a href="{% url 'editar' pessoa.id %}">Editar</a></li>
            {% endfor %}
        </ul>
    )
    # Em seguida devo criar a url editar em urls.py e importar a view editar(
        from django.contrib import admin
        from django.urls import path, include
        from .views import home, salvar, editar

        urlpatterns = [
            path('', home),
            path('salvar/', salvar, name="salvar"),
            path('editar/<int:id>', editar, nome= "editar")
        ]
    )
    # Criar view editar (
        def editar(request, id):
            pessoa = Pessoa.objects.get(id=id)
            return render(request, "update.html", {"pessoa": pessoa})
    )
    Em seguida devo criar novo template, criando um aquivo chamado update.html (
        <!-- Imprimir Pessoa -->>
        {{ pessoa.id }} - {{ pessoa.nome }}
        
        <!-- Cadastrar Pessoa nova -->
        <form action="{% url 'update' pessoa.id %}" method="POST">
            {% csrf_token %}
            <input type="text" name="nome" value="{{pessoa.nome}}">
            <button type="submit">Update</button>
        </form>
    )
    # Em seguida devo criar a url update e importar a view(
        from django.contrib import admin
        from django.urls import path, include
        from .views import home, salvar, editar, update

        urlpatterns = [
            path('', home),
            path('salvar/', salvar, name="salvar"),
            path('editar/<int:id>', editar, nome= "editar"),
            path('update/<int:id>', update, nome= "editar")
        ]
    )
    # Em seguida devo criar a view update (
        def update(request, id):
            vnome = request.POST.get("nome")
            pessoa = Pessoa.objects.get(id=id)
            pessoa.nome = vnome
            pessoa.save()
    ) 
    # Em seguida devo redirecionar ela para a home (
        from django.shortcuts import render, redirect

        def update(request, id):
            vnome = request.POST.get("nome")
            pessoa = Pessoa.objects.get(id=id)
            pessoa.nome = vnome
            pessoa.save()
            return redirect(home)
    )

### (D)ELETE ###
    # Primeiro adiciono um link para deletar a pessoa no arquivo index.html(
        <ul>
            {% for pessoa in pessoas %}
                <li>{{ pessoa.id }} - {{ pessoa.nome }}
                    <a href="{% url 'editar' pessoa.id %}">Editar</a>
                    <a href="{% url 'delete' pessoa.id %}">Deletar</a>
                </li>
            {% endfor %}
        </ul>
    )
    # Em seguida criamos a url delete e importar a view(
        from django.contrib import admin
        from django.urls import path, include
        from .views import home, salvar, editar, update, delete

        urlpatterns = [
            path('', home),
            path('salvar/', salvar, name="salvar"),
            path('editar/<int:id>', editar, name= "editar"),
            path('update/<int:id>', update, name= "update"),
            path('delete/', delete, name= "delete")
        ]
    )
    # Em seguida criamos a view para delete(
        def delete(request, id):
            pessoa = Pessoa.objects.get(id=id)
            pessoa.delete()
            return redirect(home)
    )


"""