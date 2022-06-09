from .views import *
from django.urls import path

urlpatterns = [
    path('',HomeView.as_view(),name = 'home'),
    path('subcat/<slug>',SubCategoryView.as_view(),name = 'subcat'),
    path('detail/<slug>',DetailView.as_view(),name = 'detail'),
    path('search',SearchView.as_view(),name = 'search'),
    path('signup',signup,name = 'signup'),
    path('login',login,name = 'login'),
    path('logout',logout,name = 'logout'),
    path('mycart',CartView.as_view(),name = 'mycart'),
    path('cart/<slug>',cart,name = 'cart'),
    path('delete_cart/<slug>',delete_cart,name = 'delete_cart'),
    path('remove_product/<slug>',remove_product,name = 'remove_product'),

]
