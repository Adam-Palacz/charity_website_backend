from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Institution(models.Model):
    TYPE_CHOICES = (
        (1, "fundacja"),
        (2, "organizacja pozarządowa"),
        (3, "zbiórka lokalna"),
        (4, "domyślna fundacja"),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=4)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"Nazwa instytucji: {self.name}, opis: {self.description}"


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=9)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField(null=True)
    pick_up_time = models.TimeField(null=True)
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
