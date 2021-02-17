from rest_framework.response import Response
from rest_framework import generics
from . models import Supply, Subproduct, Subproduct_supplies, Product, Product_supplies, Product_subproducts
from . serializers import SupplySerializer, SubproductSerializer, Subproduct_suppliesSerializer, ProductSerializer, Product_suppliesSerializer, Product_subproductsSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.core import serializers

class SupplyView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        header = ['Insumo', 'Unidade de Medida', 'Quantidade em Estoque', 'Custo Médio R$', 'Ação']
        raw_supplies = Supply.objects.raw("SELECT name, measure_unit, stock, average_cost, id  FROM supplies_control_supply")
        supply_list = []
        supply_list.append(header)
        for s in raw_supplies:
            dummy = []
            dummy.append(s.name)
            dummy.append(s.measure_unit)
            dummy.append(s.stock)
            dummy.append(s.average_cost)
            dummy.append(s.id)
            supply_list.append(dummy)
        return JsonResponse({'raw_data' : supply_list})

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