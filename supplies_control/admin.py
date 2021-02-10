from django.contrib import admin
from . models import Supply, Subproduct, Subproduct_supplies, Product, Product_supplies, Product_subproducts

admin.site.register(Supply)
admin.site.register(Subproduct)
admin.site.register(Subproduct_supplies)
admin.site.register(Product)
admin.site.register(Product_supplies)
admin.site.register(Product_subproducts)