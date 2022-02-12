from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import MonthData

class SaleForm(forms.ModelForm):
    class Meta:
        model = MonthData
        exclude = ['id',]
    
    def clean_product(self):
        product = self.cleaned_data.get('product')
        monthdata = self.cleaned_data.get('monthdata')
        if product not in monthdata.products.all():
            raise ValidationError('Product cannot be products of which not registered in monthdata.')
        
        return product
        

class MonthDataForm(forms.ModelForm):

    class Meta:
        model = MonthData
        exclude = ['id',]

    def clean_month(self):
        month = self.cleaned_data.get('month')
        # print(month)
        if month.day != 1:
            raise ValidationError('Month cannot of day other than 1st of the Month.')

        return month
    
    # def clean_products(self):
    #     products = self.cleaned_data.get('products')
    #     month = self.cleaned_data.get('month')
    #     print(self.cleaned_data)
    #     for product in products:
    #         if product not in MonthData.objects.filter(month=month).products.all():
    #             raise ValidationError('Product must be in monthdata!.')

    #     return products
