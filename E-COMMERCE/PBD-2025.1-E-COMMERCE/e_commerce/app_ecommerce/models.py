from unittest.mock import Base
from django.db import models

class Products(Base):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantidade_estoque = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def repor_estoque(self, quantidade):
        self.quantidade_estoque += quantidade
        self.save()

    def retirar_estoque(self, quantidade):
        if quantidade > self.quantidade_estoque:
            raise ValueError("Estoque insuficiente.")
        self.quantidade_estoque -= quantidade
        self.save()

    def category(self, categoria):
        if categoria == "ADULTO":
            self.category = categoria
        elif categoria == "INFANTIL":
            self.category = categoria
        elif categoria == "ORTOPEDICA":
            self.category = categoria
        self.save()
    

    def descricao(self):
        return f"Nome: {self.name} - Código: {self.code} - Estoque: {self.quantidade_estoque}"