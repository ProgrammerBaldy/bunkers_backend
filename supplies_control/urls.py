from django.urls import path
from . views import SupplyView, SubproductView, Subproduct_suppliesView, ProductView, Product_suppliesView, Product_subproductsView
from . import views

urlpatterns = [
    path('supplies/', SupplyView.as_view(), name="supplies_view"),
    path('subproducts/', SubproductView.as_view(), name="subproducts_view"),
]
