# Project 3

Web Programming with Python and JavaScript

## Pinocchio's Pizza Ordering System

This project was prepared to satisy project3 in the online version of this class.

## Introduction

Pinocchio's is a web application that implements an online version of the menu of the traditional Harvard Square pizza shop, Pinocchio's. The basic functions of the app are:

- *Begin (or Continue) Order*. The user can traverse a hierarchical version of the Pinoccio's menu, selecting items to order, which are placed in a virtual cart.

- *Place order.* Once the user completes ordering items, she can place her order, which records the order in the database.

- *Register, login and logout.* Before placing an order, the user must register for an account with her name and email address, and then login. When the user is finished with the app, she can logout.

- *Administrative functions.* The web app implements two such functions: bulk upload via csv file of menu items and addons, and display of all orders made by all users. In addition, the user can use the built-in Django admin app to view other information and make other changes to the data model.

These apps and web pages, how they were implemented, and how that are to be used, are all described in more detail below.

## Technologies

The app is implemented principally with Python, Javascript, and the Django framework.

## Data Structure

### Database

The app uses Django's built-in support for modeling database tables and functions. The app implements the following tables:

```python
class Category:
# Menu categories such as "Pizza," "Sicilian Pizza," Subs, and so on.

class Addon:
# Toppings (or other addons) for main menu items..
  
class MenuItem:
# Main menu items.

class OrderItem:
# Individual items in someone's order.

class PiOrder:
# Record of individual full order, including a list of OrderItems.
```

### session

The app uses session storage to hold the current shopping cart items prior to placing an order. By using session storage, the cart will be there for the user when she returns again after closing the app's window.

## How to use

The web app is started in development mode by typing `python3 manage.py runserver` in the project directory.

### Files

The following lists only files added or modified from the class distribution.

- `orders`
  - `admin.py`
  - `forms.py`
  - `models.py`
  - `urls.py`
  - `veiws.py`

- `orders/templates`
  - `adminorders.html`
  - `base.html`
  - `csv_update.html`
  - `index.html`
  - `login.html`
  - `menu1.html`
  - `menu2.html`
  - `menu3.html`
  - `register.html`
  - `showcart.html`

- `orders/static`
  - `pinocchio_72.gif`
  - `pizza.png`
  - `styles.css`

## Personal touch

The web app includes two features not called for in the project requirements.

- First is the ability of a site administrator to upload a local csv file containing MenuItem or Addon entries, which the app uses to populate the data model.
- Second is the ability of users to delete individual items in the Cart prior to placing an order.

## Instructions for using

### Home page

This page is simply a landing point to select other items from the navigation bar. The inital choices are `Home`, `Begin Order`, `Cart`, and `Login`.

### Begin order

This page displays a list of categories of menu items (Pizza, Sicilian Pizza, Subs, and so on). By continuing to click through, the user eventually arrives at specific menu items with possible options (depending on the item) such as large or small as well as toppings available. The app's menu choices here are based on the Pinocchio's menu.

Once the user has reached the last menu page and selected all options, she can click the "Add to Cart" button, which will move the item to the Cart. The user is then returned to the starting menu page to select another item, if desired. Or, the user can notice that the Cart navigation item now displays the number of items: `Cart(1)`.

Also, the `Begin Order` item has changed to `Continue Order` to reflect that the person's order is now partially complete.

### Cart

Clicking on the Cart navigation item will display any items currently in the user's Cart. If there are items in the Cart, a "Place Order" button will be enabled. If the user clicks it, and if the user is logged in, the order is recorded in the database and given an initial status of "In process." 

If the user is not logged in, she is taken to the "Login" page, which she must complete before returning to the Cart to order the items. (Items selected before login remain in the cart after the login process and can then be ordered.)

The Cart also offers the opportunity to remove any item from the Cart by clicking on the red "X" next to the item.

### Login

On this page, users can type in their usernames and passwords to log in to the site. If a user does not have an account, she can click on the "Register" link to register for the site.

### Register

On this page users can register for a new account on the system.

### Logout

Once a user has logged in, the `Login` item on the navbar changes to `Logout`.

Session and cart information, while retained if the web browser window closes or otherwise loses contact with the server, are cleared upon logout.

### Site administrator functions

If a user with "superuser" privileges (a site administrator) logs in to the web app, two new menu items become visible. These two menu items, `AdminOrders` and `UploadMenu`.

- `AdminOrders` retrieves all existing orders from anyone and displays them for the administrative user.
- `UploadMenu` displays a page that allows the administrative user to upload csv files to populate new or modified items in the MenuItem and Addon database models. If an item in the csv file has the same name as one already in the database, the existing item is replaced, allowing updates of pricing, sizes, and so on. Addons are automatically added to all MenuItems in the same Category, so if some items in the same category (such as certain Subs) do not carry the same addons as others, the administrator must update these items separately in the admin interface.
