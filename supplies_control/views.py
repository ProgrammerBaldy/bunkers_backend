from rest_framework.response import Response
from rest_framework import generics
from . models import Supply, Subproduct, Subproduct_supplies, Product, Product_supplies, Product_subproducts
from . serializers import SupplySerializer, SubproductSerializer, Subproduct_suppliesSerializer, ProductSerializer, Product_suppliesSerializer, Product_subproductsSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.core import serializers
import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status


class SupplyView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get (self, request, *args, **kwargs):
        header = ['Insumo', 'Unidade de Medida', 'Quantidade em Estoque', 'Custo Médio R$', 'Ação']
        header_keys = ['name', 'measure_unit', 'stock', 'average_cost', 'id']
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
        return JsonResponse({'raw_data' : supply_list, 'keys' : header_keys})

    def post (self, request, *args, **kwargs):
        payload = json.loads(request.body)
        try:
            supply = Supply.objects.create(
                name = payload["name"],
                measure_unit = payload["measure_unit"],
                average_cost = payload["average_cost"],
                stock = payload["stock"]
            )
            serializer = SupplySerializer(supply)
            return JsonResponse({'supply': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch (self, request, *args, **kwargs):
        payload = json.loads(request.body)
        try:
            old_supply = Supply.objects.filter(id = payload["id"])
            old_supply.update(**payload)
            supply = Supply.objects.get(id = payload["id"])
            serializer = SupplySerializer(supply)
            return JsonResponse({'supply': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Something terrible went wrong : ' + str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete (self, request, *args, **kwargs):
        payload = json.loads(request.body)
        try:
            supply = Supply.objects.filter(id = payload["id"])
            supply.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class SubproductView(generics.RetrieveAPIView):
    queryset = Subproduct.objects.all()
    
    def delete (self, request, *args, **kwargs):
        subproductid = self.kwargs.get('subproductid')
        try:
            subproduct = Subproduct.objects.filter(id = subproductid)
            subproduct.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch (self, request, *args, **kwargs):
        subproductid = self.kwargs.get('subproductid')
        payload = json.loads(request.body)
        try:
            subproduct = Subproduct.objects.get(pk=subproductid)
            
            subproduct.name = payload["name"]
            subproduct.measure_unit = payload["measure_unit"]
            subproduct.production_cost = payload["average_cost"]
            
            subproduct.stock = payload["stock"]
            
            subproduct.recipe_final_weight = payload["recipe_final_weight"]
            
            subproduct.save()
            #insert supplies
            if (Subproduct_supplies.objects.filter(subproductid_id=subproductid).exists()):
                subproduct_supplies = Subproduct_supplies.objects.get(subproductid_id=subproductid)
                for item in subproduct_supplies:
                    item.delete()
            for item in payload["supplies"]:
                subproduct_supplies = Subproduct_supplies.objects.create(
                    subproductid = subproduct,
                    supplyid = Supply.objects.get(id = item["supplyid"]),
                    quantity =  float(item["quantity"])
                )

            serializer = SubproductSerializer(subproduct)
            return JsonResponse({'subproduct': 'ok'}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Something terrible went wrong: '+str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        subproductid = self.kwargs.get('subproductid')
        raw_supplies = Subproduct.objects.raw('''SELECT sp.id, s.name, s.measure_unit, ss.quantity, s.average_cost AS total_cost, s.id AS supply_id
                                                    FROM supplies_control_subproduct sp
                                                    LEFT JOIN supplies_control_subproduct_supplies ss ON ss.subproductid_id = sp.id
                                                    LEFT JOIN supplies_control_supply s ON s.id = ss.supplyid_id
                                                    WHERE sp.id = '''+str(subproductid))
        supply_list = []
        for s in raw_supplies:
            dummy = []
            dummy.append(s.name)
            dummy.append(s.measure_unit)
            dummy.append(s.quantity)
            dummy.append(s.total_cost)
            dummy.append(s.supply_id)
            supply_list.append(dummy)
        raw_subproduct = Subproduct.objects.raw('''SELECT sp.id, sp.name, sp.measure_unit, sp.stock
                                                    FROM supplies_control_subproduct sp
                                                    WHERE sp.id = '''+str(subproductid))
        subproduct = []
        for s in raw_supplies:
            dummy = []
            dummy.append(s.name)
            dummy.append(s.measure_unit)
            dummy.append(s.stock)
            dummy.append(s.id)
            subproduct.append(dummy)
        
        return JsonResponse({'supplies' : supply_list, 'subproduct' : subproduct})

    def post (self, request, *args, **kwargs):
        payload = json.loads(request.body)
        try:
            subproduct = Subproduct.objects.create(
                name = payload["name"],
                measure_unit = payload["measure_unit"],
                production_cost = payload["average_cost"],
                stock = payload["stock"],
                recipe_final_weight = payload["recipe_final_weight"]
            )
            #insert supplies
            for item in payload["supplies"]:
                subproduct_supplies = Subproduct_supplies.objects.create(
                    subproductid = subproduct,
                    supplyid = Supply.objects.get(id = item["supplyid"]),
                    quantity = item["quantity"]
                )

            serializer = SubproductSerializer(subproduct)
            return JsonResponse({'subproduct': 'ok'}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Something terrible went wrong: '+str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Subproduct_suppliesView(generics.RetrieveAPIView):
    queryset = Subproduct_supplies.objects.all()

    def get(self, request, *args, **kwargs):
        header = ['Nome', 'Unidade de Medida', 'Quantidade em Estoque', 'Custo Médio R$', 'Ação']
        header_keys = ['name', 'measure_unit', 'stock', 'total_cost', 'id']
        raw_subproducts = Subproduct.objects.raw('''SELECT sp.name, sp.measure_unit, sp.stock, SUM(ss.quantity * s.average_cost) AS total_cost, sp.id
                                            FROM supplies_control_subproduct sp
                                            LEFT JOIN supplies_control_subproduct_supplies ss ON ss.subproductid_id = sp.id
                                            LEFT JOIN supplies_control_supply s ON s.id = ss.supplyid_id
                                            GROUP BY sp.id''')
        subproducts_list = []
        subproducts_list.append(header)
        for s in raw_subproducts:
            dummy = []
            dummy.append(s.name)
            dummy.append(s.measure_unit)
            dummy.append(s.stock)
            dummy.append(s.total_cost)
            dummy.append(s.id)
            subproducts_list.append(dummy)
        return JsonResponse({'raw_data' : subproducts_list, 'keys' : header_keys})

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