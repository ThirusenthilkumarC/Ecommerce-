from django.db import models


class Product(models.Model):

    STATUS = [
        ("Available", "Available"),
        ("Out of Stock", "Out of Stock"),
    ]

    name = models.CharField(
        max_length=100
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(
        default="No Description"
    )

    image = models.ImageField(
        upload_to="uploads/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Available"
    )

    def __str__(self):
        return self.name