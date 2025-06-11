from django.db import models
from authentication.models import User


class Category(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"Categoria:  {self.description}"


class Company(models.Model):
    id_company = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    categorys = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return f"Nome: {self.name} - CNPJ: {self.cnpj}"


class Item(models.Model):
    code_item = models.CharField(max_length=100, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.CharField(max_length=30)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='itens_images/', null=True, blank=True)

    def __str__(self):
        return f"Nome = {self.name}"

    def repor_estoque(self, quantidade):
        self.stock_quantity += quantidade
        self.save()

    def retirar_estoque(self, quantidade):
        if quantidade > self.stock_quantity:
            raise ValueError("Estoque insuficiente.")
        self.stock_quantity -= quantidade
        self.save()

    def descricao(self):
        return (
            f"Nome: {self.name} - Código: {self.code_item} - "
            f"Categoria: {self.category} - Descrição: {self.description} - "
            f"Estoque: {self.stock_quantity}"
        )
