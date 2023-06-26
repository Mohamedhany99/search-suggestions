from django.db import models
from uuid import uuid4


# Create your models here.
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    def __str__(self) -> str:
        return f"{self.name}"
