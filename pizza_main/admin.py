from django.contrib import admin
from .models import PizzaSize, CrustType, Sauce, Cheese, Topping, Pizza

admin.site.register(PizzaSize)
admin.site.register(CrustType)
admin.site.register(Sauce)
admin.site.register(Cheese)
admin.site.register(Topping)
admin.site.register(Pizza)