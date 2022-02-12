from django.contrib import admin
from django.urls import resolve

# Register your models here.
from .forms import MonthDataForm
from .models import Expense, MonthData, Sale, Product, Purchase, PreviousBalance

class ProductInline(admin.TabularInline):
    fields = ['name', 'user']
    model = Product
    extra = 3

class SaleInline(admin.TabularInline):
    fields = ['date', 'product', 'unit_price', 'quantity', 'account']
    model = Sale
    extra = 3
    ordering = ['date']

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            # retrieves the primary key via /<path:object_id>/
            return self.parent_model.objects.get(pk=int(resolved.kwargs['object_id']))
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            # obtain parent model via custom function get_parent_from_request
            monthdata = self.get_parent_object_from_request(request)
            if monthdata:
                # only lists the products that are added to the parent model
                kwargs["queryset"] = monthdata.products.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PurchaseInline(admin.TabularInline):
    fields = ['date', 'product', 'unit_price', 'quantity']
    model = Purchase
    extra = 3
    ordering = ['date']


    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            # retrieves the primary key via /<path:object_id>/
            return self.parent_model.objects.get(pk=int(resolved.kwargs['object_id']))
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            # obtain parent model via custom function get_parent_from_request
            monthdata = self.get_parent_object_from_request(request)
            if monthdata:
                # only lists the products that are added to the parent model
                kwargs["queryset"] = monthdata.products.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ExpenseInline(admin.TabularInline):
    fields = ['date', 'description', 'unit_price', 'quantity']
    model = Expense
    extra = 3

class PreviousBalanceInline(admin.TabularInline):
    fields = ['product', 'unit_price', 'quantity']
    model = PreviousBalance
    extra = 3

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        if resolved.kwargs:
            # retrieves the primary key via /<path:object_id>/
            return self.parent_model.objects.get(pk=int(resolved.kwargs['object_id']))
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            # obtain parent model via custom function get_parent_from_request
            monthdata = self.get_parent_object_from_request(request)
            if monthdata:
                # only lists the products that are added to the parent model
                kwargs["queryset"] = monthdata.products.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(MonthData)
class MonthDataAdmin(admin.ModelAdmin):
    form = MonthDataForm
    inlines = [PurchaseInline, SaleInline, ExpenseInline, PreviousBalanceInline]
    filter_horizontal = ('products',)
    list_display = ('id', 'user', 'month')

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name', 'user']
    readonly_fields = ['id',]

admin.site.register(Product, ProductAdmin)
