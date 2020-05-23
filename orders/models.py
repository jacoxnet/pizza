from django.db import models

# Create your models here.

class Addon(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    PIZZA = 1
    SUB = 2
    type = models.PositiveSmallIntegerField(choices=[(PIZZA, "Pizza"), (SUB, "Sub")])

    def __str__(self):
        if self.type == self.PIZZA:
            return f"{self.name} for Pizza"
        else:
            return f"{self.name} for Sub"

class MenuItem(models.Model):
    PIZZA = 1
    SICILIAN = 2
    SUB = 4
    PASTA = 6
    SALAD = 7
    DINNER_PLATTER = 8
    CATEGORY_CHOICES = [(PIZZA, "Pizza"), (SICILIAN, "Sicilian Pizza"), 
                   (SUB, "Sub"), (PASTA, "Pasta"), (SALAD, "Salad"), 
                   (DINNER_PLATTER, "Dinner Platter")]
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=64)
    LARGE = "L"
    SMALL = "S"
    NOSIZE = "N"
    size = models.CharField(max_length=1, 
                            choices=[(LARGE, "Large"), (SMALL, "Small"), (NOSIZE, "No Size")])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    addon = models.ManyToManyField(Addon, blank=True)

    def __str__(self):
        p = ""
        for n, v in self.CATEGORY_CHOICES:
            if n == self.category:
                p = v
                break
        p = p + " '" + self.name + "' " + self.size
        return p

class Customer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField
    password = models.CharField(max_length=64)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ManyToManyField(MenuItem, blank=True)
    time = models.DateTimeField
    price = models.DecimalField(max_digits=6, decimal_places=2)