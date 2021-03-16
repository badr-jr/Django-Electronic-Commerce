from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create_list,name="create_list"),
    path("listing/<int:lis_id>",views.show_listing,name="show_listing"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("category/<str:categ>",views.show_categories,name="category")
]
