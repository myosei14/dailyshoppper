from django.db import models


class Product(models.Model):
    product = models.CharField(max_length=250)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True)
    categories = (
        ('1', 'Category 1'),
        ('2', 'Category 2'),
        ('3', 'Category 3'),
        ('4', 'Category 4')
    )
    category = models.CharField(max_length=20, choices=categories)

    def __str__(self):
        return self.product


