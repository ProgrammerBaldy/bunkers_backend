from django.db import models

class Supply (models.Model):
    name = models.CharField(max_length=255)
    measure_unit = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Subproduct (models.Model):
    name = models.CharField(max_length=255)
    measure_unit = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Subproduct_supplies (models.Model):
    subproductid = models.ForeignKey(Subproduct, on_delete=models.CASCADE, null=False)
    supplyid = models.ForeignKey(Supply, on_delete=models.CASCADE, null=False)

class Product (models.Model):
    name = models.CharField(max_length=255)
    measure_unit = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product_supplies (models.Model):
    productid = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    supplyid = models.ForeignKey(Supply, on_delete=models.CASCADE, null=False)

class Product_subproducts (models.Model):
    productid = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    subproductid = models.ForeignKey(Subproduct, on_delete=models.CASCADE, null=False)