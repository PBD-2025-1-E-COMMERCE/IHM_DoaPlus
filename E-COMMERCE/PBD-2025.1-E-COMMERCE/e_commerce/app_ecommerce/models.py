from django.db import models
from authentication.models import User


class Category(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"Categoria:  {self.description} "
    
class Color(models.Model):
    color = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.color}"
    
class Size(models.Model):
    size = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.size}"

class Storage(models.Model):
    storage = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.storage}"
class Company(models.Model):
    id_company = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    logo = models.ImageField(upload_to='itens_images/', null=True, blank=True)

    def __str__(self):
        return f"Nome: {self.name} - CNPJ: {self.cnpj}"


class Item(models.Model):
    code_item = models.CharField(max_length=100, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    level = models.CharField(max_length=30)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='itens_images/', null=True, blank=True)

    def __str__(self):
        return f"Nome = {self.name}"


class Image(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='itens_images/')

    def __str__(self):
        return f"Imagem de {self.item.name}"

class ItemDetails(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    size = models.ForeignKey(Size, on_delete=models.PROTECT)
    storage = models.ForeignKey(Storage, on_delete=models.PROTECT)

    def __str__(self):
        return f" {self.color} - {self.size} - {self.storage}"