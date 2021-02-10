from rest_framework import serializers
from . models import Supply, Subproduct, Subproduct_supplies, Product, Product_supplies, Product_subproducts

class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = '__all__'

class SubproductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subproduct
        fields = '__all__'

class Subproduct_suppliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subproduct_supplies
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class Product_suppliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_supplies
        fields = '__all__'

class Product_subproductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_subproducts
        fields = '__all__'