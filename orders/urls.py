from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("menu1/", views.menu1, name="menu1"),
    path("menu2/", views.menu2, name="menu2"),
    path("menu3/", views.menu3, name="menu3"),
    path("addcart/", views.addcart, name="addcart"),
    path("displaycart/", views.displaycart, name="displaycart"),
    path("<int:cartnum>/deletecartitem/", views.deletecartitem, name="deletecartitem"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("placeorder/", views.placeorder, name="placeorder"),
    path("upload/", views.upload, name="upload"),
    path("adminorders/", views.adminorders, name="adminorders")
]