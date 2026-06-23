from django.db import models
from authentication.models import User


class Category(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.description} "


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
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

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
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"Nome = {self.name}"


class ItemDetails(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    size = models.ForeignKey(
        Size, on_delete=models.PROTECT, blank=True, null=True)
    storage = models.ForeignKey(
        Storage, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f" {self.color} - {self.size} - {self.storage}"


class Ongs(models.Model):
    name = models.CharField(max_length=100)


class Causa(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=450, null=False, blank=False)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_arrecadado = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    porcentagem = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    ativo = models.BooleanField(default=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    ong = models.ForeignKey(
        Ongs, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(
        upload_to='itens_images/', null=True, blank=True)


class Cupom(models.Model):

    codigo = models.CharField(max_length=20, unique=True)

    desconto = models.DecimalField(max_digits=5, decimal_places=2)

    tipo_desconto = models.CharField(
        max_length=4,
        choices=[
            ('PERC', 'Porcentagem'),
            ('FIXO', 'Valor Fixo')
        ]
    )

    validade = models.DateTimeField()
    usado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo


class Image(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='image_item',
        null=True,
        blank=True
    )

    causa = models.ForeignKey(
        Causa,
        on_delete=models.CASCADE,
        related_name='imagem_causa',
        null=True,
        blank=True
    )

    image = models.ImageField(upload_to='itens_images/')
