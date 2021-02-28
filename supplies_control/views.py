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
                subproduct_supplies = Subproduct_supplies.objects.all().filter(subproductid_id=subproductid)
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
        raw_subproduct = Subproduct.objects.raw('''SELECT sp.id, sp.name, sp.measure_unit, sp.stock, sp.recipe_final_weight
                                                    FROM supplies_control_subproduct sp
                                                    WHERE sp.id = '''+str(subproductid))
        subproduct = []
        for s in raw_subproduct:
            dummy = []
            dummy.append(s.name)
            dummy.append(s.measure_unit)
            dummy.append(s.stock)
            dummy.append(s.id)
            dummy.append(s.recipe_final_weight)
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
        header = ['Nome', 'Unidade de Medida', 'Peso Pronto', 'Quantidade em Estoque', 'Custo Médio R$', 'Ação']
        header_keys = ['name', 'measure_unit', 'recipe_final_weight', 'stock', 'total_cost', 'id']
        raw_subproducts = Subproduct.objects.raw('''SELECT sp.name, sp.measure_unit, sp.stock, SUM(ss.quantity * s.average_cost) AS total_cost, sp.recipe_final_weight, sp.id
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
            dummy.append(s.recipe_final_weight)
            dummy.append(s.stock)
            dummy.append(s.total_cost)
            dummy.append(s.id)
            subproducts_list.append(dummy)
        return JsonResponse({'raw_data' : subproducts_list, 'keys' : header_keys})




class ProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()

    def delete (self, request, *args, **kwargs):
        productid = self.kwargs.get('productid')
        try:
            product = Product.objects.filter(id = productid)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch (self, request, *args, **kwargs):
        productid = self.kwargs.get('productid')
        payload = json.loads(request.body)
        try:
            product = Product.objects.get(pk=productid)
            product.name = payload["name"]
            product.measure_unit = payload["measure_unit"]
            product.production_cost = 0
            product.stock = payload["stock"]
            product.selling_price = payload["selling_price"]

            product.save()
            print(Product_supplies.objects.filter(productid_id=productid).exists())
            if (Product_supplies.objects.filter(productid_id=productid).exists()):
                product_supplies = Product_supplies.objects.all().filter(productid_id=productid)
                print(product_supplies)
                for item in product_supplies:
                    print(item.pk)
                    item.delete()

            #insert supplies
            for item in payload["supplies"]:
                print (item)
                product_supplies = Product_supplies.objects.create(
                    productid = product,
                    supplyid = Supply.objects.get(id = item["supplyid"]),
                    quantity = item["quantity"]
                )


            if (Product_subproducts.objects.filter(productid_id=productid).exists()):
                product_subproducts = Product_subproducts.objects.all().filter(productid_id=productid)
                for item in product_subproducts:
                    item.delete()
            #insert subproducts
            for item in payload["subproducts"]:
                product_subproducts = Product_subproducts.objects.create(
                    productid = product,
                    subproductid = Subproduct.objects.get(id = item["subproductid"]),
                    quantity = item["quantity"]
                )

            serializer = SubproductSerializer(product)
            return JsonResponse({'product': 'ok'}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Something terrible went wrong: '+str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        productid = self.kwargs.get('productid')
        raw_supplies = Product.objects.raw('''SELECT p.id, s.name, s.measure_unit, ps.quantity, s.id AS supply_id
                                                FROM supplies_control_product p
                                                LEFT JOIN supplies_control_product_supplies ps ON ps.productid_id = p.id
                                                LEFT JOIN supplies_control_supply s ON s.id = ps.supplyid_id
                                                WHERE p.id = '''+str(productid))
        supply_list = []
        for s in raw_supplies:
            dummy = []
            dummy.append(s.name)
            dummy.append(s.measure_unit)
            dummy.append(s.quantity)
            dummy.append(s.supply_id)
            supply_list.append(dummy)


        raw_subproducts = Product.objects.raw('''SELECT p.id, sp.name, sp.measure_unit, psp.quantity, sp.id AS supply_id
                                                FROM supplies_control_product p
                                                LEFT JOIN supplies_control_product_subproducts psp ON psp.productid_id = p.id
                                                LEFT JOIN supplies_control_subproduct sp ON sp.id = psp.subproductid_id
                                                WHERE p.id = '''+str(productid))
        subproducts = []
        for sp in raw_subproducts:
            dummy = []
            dummy.append(sp.name)
            dummy.append(sp.measure_unit)
            dummy.append(sp.quantity)
            dummy.append(sp.supply_id)
            subproducts.append(dummy)

        raw_products = Product.objects.raw('''SELECT p.id, p.name, p.measure_unit, p.stock, p.selling_price
                                                FROM supplies_control_product p
                                                WHERE p.id = '''+str(productid))
        product = []
        for p in raw_products:
            dummy = []
            dummy.append(p.name)
            dummy.append(p.measure_unit)
            dummy.append(p.stock)
            dummy.append(p.selling_price)
            dummy.append(p.id)
            product.append(dummy)
        
        return JsonResponse({'supplies' : supply_list, 'subproducts' : subproducts, 'product' : product})

    def post (self, request, *args, **kwargs):
        payload = json.loads(request.body)
        try:
            product = Product.objects.create(
                name = payload["name"],
                measure_unit = payload["measure_unit"],
                production_cost = 0,
                stock = payload["stock"],
                selling_price = payload["selling_price"]
            )
            #insert supplies
            for item in payload["supplies"]:
                print (item)
                product_supplies = Product_supplies.objects.create(
                    productid = product,
                    supplyid = Supply.objects.get(id = item["supplyid"]),
                    quantity = item["quantity"]
                )
            #insert subproducts
            for item in payload["subproducts"]:
                print (item)
                product_subproducts = Product_subproducts.objects.create(
                    productid = product,
                    subproductid = Subproduct.objects.get(id = item["subproductid"]),
                    quantity = item["quantity"]
                )

            serializer = SubproductSerializer(product)
            return JsonResponse({'product': 'ok'}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': 'Something terrible went wrong: '+str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Product_suppliesView(generics.RetrieveAPIView):
    queryset = Product_supplies.objects.all()

    def get(self, request, *args, **kwargs):
        header = ['Nome', 'Preço de Venda', 'Custo Médio R$', 'Ação']
        header_keys = ['name', 'selling_price', 'cost', 'id']
        raw_products = Product.objects.raw('''SELECT dummy.name, dummy.selling_price, SUM(dummy.cost) AS cost, dummy.id
                                                    FROM (
                                                        (SELECT p.id, p.name, p.measure_unit, p.stock, p.selling_price AS selling_price,
                                                        SUM(s.average_cost * ps.quantity) AS cost
                                                        FROM supplies_control_product p
                                                        LEFT JOIN supplies_control_product_supplies ps ON ps.productid_id = p.id
                                                        LEFT JOIN supplies_control_supply s ON s.id = ps.supplyid_id
                                                        GROUP BY p.id)

                                                        UNION ALL 

                                                        (SELECT p.id, p.name, p.measure_unit, p.stock, p.selling_price AS selling_price,
                                                        SUM(s.average_cost * ss.quantity) AS cost
                                                        FROM supplies_control_product p
                                                        INNER JOIN supplies_control_product_subproducts psp ON p.id = psp.productid_id
                                                        LEFT JOIN supplies_control_subproduct sp ON sp.id = psp.subproductid_id
                                                        LEFT JOIN supplies_control_subproduct_supplies ss ON ss.subproductid_id = sp.id
                                                        LEFT JOIN supplies_control_supply s ON s.id = ss.supplyid_id
                                                        GROUP BY p.id)
                                                    ) dummy
                                                    GROUP BY dummy.id, dummy.name, dummy.measure_unit, dummy.stock, dummy.selling_price''')
        products_list = []
        products_list.append(header)
        for p in raw_products:
            dummy = []
            dummy.append(p.name)
            dummy.append(p.selling_price)
            dummy.append(p.cost)
            dummy.append(p.id)
            products_list.append(dummy)
        return JsonResponse({'raw_data' : products_list, 'keys' : header_keys})

class Product_subproductsView(generics.RetrieveAPIView):
    queryset = Product_subproducts.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = Product_subproductsSerializer(queryset, many=True)
        return Response(serializer.data)