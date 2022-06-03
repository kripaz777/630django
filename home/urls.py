from .views import *
from django.urls import path

urlpatterns = [
    path('',HomeView.as_view(),name = 'home'),
    path('subcat/<slug>',SubCategoryView.as_view(),name = 'subcat'),
    path('detail/<slug>',DetailView.as_view(),name = 'detail'),

]
