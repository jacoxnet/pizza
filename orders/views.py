from django.http import HttpResponse, Http404
from django.shortcuts import render

from .models import MenuItem, Addon

# Create your views here.
def index(request):
    context = {
        "fullmenu": MenuItem.objects.all()
    }
    return render(request, "orders/index.html", context)

def singleitem(request, item_id):
    try:
        item = MenuItem.objects.get(pk=item_id)
    except MenuItem.DoesNotExist:
        raise Http404("MenuItem does not exist")
    context = {
        "item": item
    }
    return render(request, "orders/singleitem.html", context)