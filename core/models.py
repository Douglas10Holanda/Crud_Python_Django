from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)

# Método para mostrar o nome da pessoa
    def __str__(self):
        return self.nome
