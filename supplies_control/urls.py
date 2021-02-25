from django.urls import path
from . views import SupplyView, SubproductView, Subproduct_suppliesView, ProductView, Product_suppliesView, Product_subproductsView
from . import views

urlpatterns = [
    path('supplies/', SupplyView.as_view(), name="supplies_view"),
    path('subproducts/', SubproductView.as_view(), name="subproducts_view"),
    path('subproducts/<int:subproductid>', SubproductView.as_view(), name="subproducts_view"),
    path('subproducts_supplies/', Subproduct_suppliesView.as_view(), name="subproducts_supplies_view"),
    path('products/<int:productid>', ProductView.as_view(), name="products_view"),
    path('products/', ProductView.as_view(), name="products_view"),
]
