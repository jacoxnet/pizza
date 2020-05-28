from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

import csv
from datetime import datetime

from .forms import UploadFileForm
from .models import MenuItem, Addon, Category, PiOrder, OrderItem

# Create your views here.

# route /
def index(request):
    cart = int(request.session.get('cart', 0))
    if cart == 0:
        request.session["cart"] = 0
        request.session["cart_items"] = []
    context = {
        "cart": cart
    }
    return render(request, "orders/index.html", context)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.INFO, "Login successful")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(request, messages.INFO, "Login unsuccessful")
            return render(request, "orders/login.html")
    else:
        context = {
           "cart": request.session.get("cart")
        }
        return render(request, "orders/login.html", context)

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Logged out")
    return HttpResponseRedirect(reverse("index"))

def register(request):
    """Register new user"""
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        passagain = request.POST["passagain"]

        if username == "":
            messages.add_message(request, messages.INFO, "Please provide a username")
            return HttpResponseRedirect(reverse("register"))
        elif password == "":
            messages.add_message(request, messages.INFO, "Please provide a password")
            return HttpResponseRedirect(reverse("register"))
        elif password != passagain:
            messages.add_message(request, messages.INFO, "Password fields don't match")
            return HttpResponseRedirect(reverse("register"))
        username = username.lower()
        try: 
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
        except:
            messages.add_message(request, messages.INFO, "Error adding user")
            return HttpResponseRedirect(reverse("register"))
        # Redirect user to home page
        messages.add_message(request, messages.INFO, "Registration successful")
        return HttpResponseRedirect(reverse("index"))
    else:
        context = {
           "cart": request.session.get("cart")
        }
        return render(request, "orders/register.html", context)

# route menu1/
def menu1(request):
    cart = int(request.session.get('cart'))
    # Create list of categories to pass to template
    # first two should be the pizzas
    category_list = ["Pizza", "Sicilian Pizza"]
    # get rest excluding pizzas
    category_list += [x.type for x in Category.objects.exclude(type__icontains="pizza")]
    context = {
        "cart": cart,
        "categories": category_list
    }
    return render(request, "orders/menu1.html", context)

# route menu2/
def menu2(request):
    cart = int(request.session.get('cart'))
    category = request.POST["selectcat"]
    items = MenuItem.objects.filter(category__type=category)
    context = {
        "cart": cart,
        "category": category,
        "items": items
    }
    return render(request, "orders/menu2.html", context)

# route menu3/
def menu3(request):
    cart = int(request.session.get('cart'))
    id = request.POST["selectitem"]
    print(request.POST.keys())
    item = MenuItem.objects.get(pk=id)
    context = {
        "cart": cart,
        "item": item,
        "addons": item.addons.all(),
        "alimit": item.alimit
    }
    return render(request, "orders/menu3.html", context)

# route addcart/
# add selected items to cart
def addcart(request):
    # on return from submit button to add to cart, 
    # add item to cart in session dict
    cart = int(request.session.get("cart"))
    item_id = request.POST["item_id"]
    size = request.POST["size"]
    # retrieve menuitem from id
    item = MenuItem.objects.get(pk=item_id)
    if size == "small":
        price = item.priceS
    else:
        price = item.priceL
    if not item.sized:
        size = "one size"
    # make list of selected addons and add price of each
    addons = []
    for a in item.addons.all():
        if a.name in request.POST.keys():
            addons.append(a.name)
            price += a.price
    # add to session cart
    value = {
        "id": item.id,
        "name": item.name,
        "size": size,
        "addons": ", ".join(addons),
        "price": float(price)
    }
    request.session["cart_items"].append(value)
    request.session.modified = True
    cart += 1
    request.session["cart"] = cart
    messages.add_message(request, messages.INFO, "Item successfully added to cart")
    return HttpResponseRedirect(reverse("menu1"))
    
# route displaycart/
def displaycart(request):
    cart = request.session.get("cart")
    cart_items = request.session.get("cart_items")
    total_price = 0
    for item in cart_items:
        total_price += item["price"]
    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price
    }
    return render(request, "orders/showcart.html", context)

# route deletecartitem/
def deletecartitem(request, cartnum):
    cart = request.session.get("cart")
    cart_items = request.session.get("cart_items")
    del cart_items[cartnum]
    cart -= 1
    request.session["cart_items"] = cart_items
    request.session["cart"] = cart
    return HttpResponseRedirect(reverse("displaycart"))

# route placeorder/
def placeorder(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please login first")
        return render(request, "orders/login.html")
    user = request.user
    cart_items = request.session.get("cart_items")
    total_price = 0
    order = PiOrder(user=user, time=datetime.now(), status="In Process")
    order.save()
    for item in cart_items:
        orderitem = OrderItem(name=item["name"], menu_id=item["id"], size=item["size"], price=item["price"], addons=item["addons"])
        orderitem.save()
        order.items.add(orderitem)
        total_price += item["price"]
    order.price = total_price
    order.save()
    request.session["cart"] = 0
    request.session["cart_items"] = []
    messages.add_message(request, messages.INFO, "Order recorded")
    return HttpResponseRedirect(reverse("index"))
    
# route adminorders/
def adminorders(request):
    allorders = PiOrder.objects.all()
    context = {
        "allorders": allorders
    }
    return render(request, "orders/adminorders.html", context)

# route upload/
def upload(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.INFO, "Please login as superuser first")
        return render(request, "orders/login.html")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(f"cvs: keys of post request {request.POST.keys()}")
            f = request.FILES["csvfile"]
            f.open(mode="r")
            fr = f.read()
            fr = fr.decode("UTF-8")
            lines = fr.splitlines()
            reader = csv.reader(lines)
            parsed_csv = list(reader)
            ncount = 0
            mcount = 0
            if "menuitem" in request.POST:
                # should be seeing category.type, name, sized, priceS, priceL, alimit
                for p in parsed_csv:
                    # create category if necessary
                    if len(Category.objects.filter(type=p[0])) == 0:
                        c = Category(type=p[0])
                        c.save()
                    # does entry already exist with category & name?
                    m = MenuItem.objects.filter(category__type=p[0], name=p[1])
                    if len(m) == 0:
                        # create new record
                        x = MenuItem(category=Category.objects.get(type=p[0]), name=p[1], sized=(p[2] == "TRUE"), priceS=float(p[3]), priceL=float(p[4]), alimit=int(p[5]))
                        x.save()
                        ncount += 1
                    else:
                        # update prices in old record
                        m[0].priceS=float(p[3])
                        m[0].priceL=float(p[4])
                        m[0].alimit=int(p[5])
                        m[0].save()
                        mcount += 1
                messages.add_message(request, messages.INFO, f"Successfully added {ncount} new and {mcount} modified MenuItem records")
                return HttpResponseRedirect(reverse("index"))
            else:
                # if not menuitem update addons
                # should be seeing name, price, category.type
                for p in parsed_csv:
                    # does entry already exist with name?
                    a = Addon.objects.filter(name=p[0])
                    if len(a) == 0:
                        # create new record
                        x = Addon(name=p[0], price=float(p[1]))
                        x.save()
                        ncount += 1
                    else:
                        x = a[0]
                        # update price on old record
                        x.price = float(p[1])
                        x.save()
                        mcount += 1
                    # add (or re-add) x to all MenuItem records where category type is p[2]
                    for m in MenuItem.objects.filter(category=Category.objects.get(type=p[2])):
                        m.addons.add(x)
                messages.add_message(request, messages.INFO, f"Successfully added {ncount} new and {mcount} modified Addon records")
                return HttpResponseRedirect(reverse("index"))
    else:
        # called by GET request
        form = UploadFileForm()
        return render(request, 'orders/csv_update.html', {'form': form})