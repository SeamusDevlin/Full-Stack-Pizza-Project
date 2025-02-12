from django import forms
from datetime import date
from .models import PizzaSize, CrustType, Sauce, Cheese, Topping

class PizzaForm(forms.Form):
    size = forms.ModelChoiceField(queryset=PizzaSize.objects.all())
    crust = forms.ModelChoiceField(queryset=CrustType.objects.all())
    sauce = forms.ModelChoiceField(queryset=Sauce.objects.all())
    cheese = forms.ModelChoiceField(queryset=Cheese.objects.all())
    toppings = forms.ModelMultipleChoiceField(
        queryset=Topping.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class OrderForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    card_number = forms.CharField(max_length=16, min_length=16)
    card_expiry_month = forms.IntegerField(min_value=1, max_value=12)
    card_expiry_year = forms.IntegerField(min_value=2025, max_value=2040)
    card_cvv = forms.CharField(max_length=3, min_length=3)

    def clean(self):
        cleaned_data = super().clean()
        expiry_month = cleaned_data.get('card_expiry_month')
        expiry_year = cleaned_data.get('card_expiry_year')

        if expiry_month and expiry_year:
            today = date.today()
            if expiry_year < today.year or (expiry_year == today.year and expiry_month < today.month):
                raise forms.ValidationError("The card expiry date is invalid.")