from rest_framework.response import Response
from rest_framework import generics
from . models import Supply, Subproduct, Subproduct_supplies, Product, Product_supplies, Product_subproducts
from . serializers import SupplySerializer, SubproductSerializer, Subproduct_suppliesSerializer, ProductSerializer, Product_suppliesSerializer, Product_subproductsSerializer
from rest_framework.permissions import IsAuthenticated


class SupplyView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Supply.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = SupplySerializer(queryset, many=True)
        return Response(serializer.data)

class SubproductView(generics.RetrieveAPIView):
    queryset = Subproduct.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = SubproductSerializer(queryset, many=True)
        return Response(serializer.data)

class Subproduct_suppliesView(generics.RetrieveAPIView):
    queryset = Subproduct_supplies.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = Subproduct_suppliesSerializer(queryset, many=True)
        return Response(serializer.data)

class ProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

class Product_suppliesView(generics.RetrieveAPIView):
    queryset = Product_supplies.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = Product_suppliesSerializer(queryset, many=True)
        return Response(serializer.data)

class Product_subproductsView(generics.RetrieveAPIView):
    queryset = Product_subproducts.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = Product_subproductsSerializer(queryset, many=True)
        return Response(serializer.data)