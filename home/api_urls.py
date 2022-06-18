from django.urls import path, include
from rest_framework import routers,viewsets
from .views import *



router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('product_filter/',ProductFilterViewSet.as_view(),name = 'product_filter'),
    path('crud_product/<int:pk>',CRUDItemViewSet.as_view(),name = 'crud_product'),
]