# Project 3

Web Programming with Python and JavaScript

## Pinocchio's Pizza Ordering System

This project was prepared to satisy project3 in the online version of this class.

## Introduction

Pinocchio's is a web application that implements an online version of the menu of the traditional Harvard Square pizza shop, Pinocchio's. The basic functions of the app are:

- *Begin (or Continue) Order*. The can traverse a hierarchical version of the Pinoccio's menu, selecting items to order, which are placed in a virtual cart.

- *Place order.* Once the user completes ordering items, she can "place the order," which records the order in the database.
- *Register, login and logout.* Before placing an order, the user must register for an account with her name and email address, and then login. When the user is finished with the app, she can logout.
- *Administrative functions.* The web app itself implements two such functions: bulk upload via csv file of menu items and addons, and display of all orders made by all users. In addition, the user can use the built-in Django admin app to view other information and make other changes to the data model.

These apps and web pages, how they were implemented, and how that are to be used, are all described in more detail below.

## Technologies

The app is implemented principally with Python, Javascript, and the Django framework.

## Data Structure

The app uses Django's built-in support for modeling database tables and functions. The app implements the following tables:

```python
class Category:
  # This table contains the menu "categories," such as "Pizza," "Sicilian Pizza," and so on. The value is stored in a string. The structure is flexibly designed so that additional categories (*e.g.*, "Dessert") can be added, which would become available for menues
class Addon:
  # This table contains all menu item "addons," which at present means toppings for pizza and subs. However, the functionality is generlizable to any addons -- free or at a cost -- to main menu items.
  
class MenuItem:
  # table for the main menu items (at present, pizzas, Sicilian pizzas, subs, salads, pasta, and dinner platters). The functionality is generlizable to other kinds of items.

class OrderItem:
  # contains individual items that make up someone's order. In many cases, the fields here are similar to those in MenuItem, but the app tracks orders separately becauase updates to MenuItem records should not change the retrieved order hisory.
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
    # status should be "In Process", "Canceled", or "Completed"
    status = models.CharField(max_length=25, blank=True)

    def __str__(self):
        s = str(self.user) + " (" + self.time.strftime("%d-%m-%y %H%M") + "), $" + str(self.price) + ", " + str(self.items.count()) + " items" + ", " + self.status
        return s
```

