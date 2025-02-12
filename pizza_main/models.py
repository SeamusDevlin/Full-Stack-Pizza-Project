from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Model for Pizza Sizes (e.g., Small, Medium, Large)
class PizzaSize(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Model for Crust Types (e.g., Normal, Thin, Thick)
class CrustType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Model for Sauces (e.g., Tomato, BBQ)
class Sauce(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Model for Cheese Types (e.g., Mozzarella, Vegan, Low Fat)
class Cheese(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Model for Toppings (e.g., Pepperoni, Chicken, Ham, Pineapple, Peppers, Mushrooms, Onions)
class Topping(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Model for Pizza Orders
class Pizza(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(PizzaSize, on_delete=models.CASCADE)
    crust = models.ForeignKey(CrustType, on_delete=models.CASCADE)
    sauce = models.ForeignKey(Sauce, on_delete=models.CASCADE)
    cheese = models.ForeignKey(Cheese, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping)
    created_at = models.DateTimeField(default=now)
    name = models.CharField(max_length=100, default="Gordon Ramsay")
    address = models.TextField(default="DCU")
    
    def __str__(self):
        return f"Pizza: {self.size}, {self.crust}, {self.sauce}, {self.cheese}, Toppings: {', '.join([topping.name for topping in self.toppings.all()])}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Order for {self.name} - {self.address}"