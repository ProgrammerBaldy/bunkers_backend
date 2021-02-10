from django.urls import path
from . views import SupplyView, SubproductView, Subproduct_suppliesView, ProductView, Product_suppliesView, Product_subproductsView

urlpatterns = [
    path('supplies/', SupplyView.as_view(), name="supplies_view")
]
