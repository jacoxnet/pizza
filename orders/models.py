from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    # Categories of MenuItems
    # Known categories now are 
    #   Pizza
    #   Sicilian Pizza
    #   Pasta
    #   Salads
    #   Subs
    #   Dinner Platters,
    type = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.type

class Addon(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sized = models.BooleanField(default=True)
    priceS = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    priceL = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    addons = models.ManyToManyField(Addon, blank=True)
    alimit = models.SmallIntegerField(null=True)

    def __str__(self):
        s = str(self.category) + " " + self.name
        if self.sized:
            s += " Small ($" + str(self.priceS) + ") Large ($" + str(self.priceL) + ")"
        else:
            s += " ($" + str(self.priceS) + ")"
        return s

# One entry on someone's order
# these must be separate from MenuItems because 
# they shouldn't change with future menu updates
class OrderItem(models.Model):
    name = models.CharField(max_length=100)
    menu_id = models.SmallIntegerField(null=True)
    size = models.CharField(max_length=25)
    # addons is just a comma-separated text field
    addons = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        s = self.name + " (#" + str(self.menu_id) + ") (" + self.size + ") ($" + str(self.price) + ")"
        if self.addons:
            s = s + " add:" + self.addons
        return s

# Someone's full order
class PiOrder(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    time = models.DateTimeField(null=True)
    items = models.ManyToManyField(OrderItem, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    # status should be "In cart" "In process", "canceled", or "completed"
    # In cart
    status = models.CharField(max_length=25, blank=True)

    def __str__(self):
        s = str(self.user) + " (" + self.time.strftime("%d-%m-%y %H%M") + "), $" + str(self.price) + ", " + str(self.items.count()) + " items" + ", " + self.status
        return s
