from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueForDateValidator

from .models import (Expense, MonthData, PreviousBalance, Product, Purchase,
                     Sale)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'user']
        read_only_fields = ['user']

class SaleSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    account = serializers.CharField(source='account.username', read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'monthdata', 'date', 'product', 'unit_price', 'quantity', 'account']
        read_only_fields = ['account']

    def validate(self, data):
        """
        Checks if Sale's `date` is within monthdata's `Month`.
        """
        monthdata = data.get('monthdata')
        date = data.get('date')
        if monthdata.month.month != date.month:
            context = {'date': 'Date for sale can only be within the current month.'}
            raise serializers.ValidationError(context)
        return data

    def create(self, validated_data):
        """
        Attempts to convert serialized product name into a product object
        and then create a Sale object with said object.
        """
        monthdata = self.validated_data.get('monthdata')
        products = monthdata.products.all()
        curr_product_name = self.validated_data.get('product')['name']
        for product in products:
            if product.name == curr_product_name:
                validated_data['product'] = product
                return Sale.objects.create(**validated_data)
        raise serializers.ValidationError(
            {
                'product': f'Invalid product.\'{curr_product_name}\' does'
                         ' not exist within this month.'
            }
        )

class PurchaseSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    class Meta:
        model = Purchase
        fields = ['id', 'monthdata', 'date', 'product', 'unit_price', 'quantity']

    def create(self, validated_data):
        """
        Attempts to convert serialized product name into a product object
        and then create a Sale object with said object.
        """
        monthdata = self.validated_data.get('monthdata')
        products = monthdata.products.all()
        curr_product_name = self.validated_data.get('product')['name']
        for product in products:
            if product.name == curr_product_name:
                validated_data['product'] = product
                purchaseobj = Purchase(**validated_data)
                try:
                    purchaseobj.clean()
                except ValidationError as err:
                    raise serializers.ValidationError(err.message)
                else:
                    purchaseobj.save()
                    return purchaseobj
        raise serializers.ValidationError(
            f'Invalid product.\'{curr_product_name}\' does not exist within this month.'
        )

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'monthdata', 'date', 'description', 'unit_price', 'quantity', 'created']

class PreviousBalanceSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    class Meta:
        model = PreviousBalance
        fields = ['id', 'monthdata', 'product', 'unit_price', 'quantity']

    def create(self, validated_data):
        """
        Attempts to convert serialized product name into a product object
        and then create a Sale object with said object.
        """
        monthdata = self.validated_data.get('monthdata')
        products = monthdata.products.all()
        curr_product_name = self.validated_data.get('product')['name']
        for product in products:
            if product.name == curr_product_name:
                validated_data['product'] = product
                try:
                    return PreviousBalance.objects.create(**validated_data)
                except IntegrityError:
                    raise serializers.ValidationError('Product already exist in monthdata.')
        raise serializers.ValidationError(
            f'Invalid product.\'{curr_product_name}\' does not exist within this month.'
        )

class MonthDataProductsField(serializers.RelatedField):

    @property
    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user

    def get_queryset(self):
        return Product.objects.filter(user=self._user)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(name=data)
        except Product.DoesNotExist as error:
            raise serializers.ValidationError(f"Invalid product {data}") from error

    def to_representation(self, value):
        return value.name

class MonthDataPatchSerializer(serializers.ModelSerializer):
    """
    Serializer for patch() of view MonthDataDetail
    Needed a different serializer for handling `PATCH` requests.
    """
    class Meta:
        model = MonthData
        fields = ['id', 'month', 'user', 'starting_modal', 'cashout', 'profit_balance']
        read_only_fields = ['user', 'month']

class MonthDataListSerializer(serializers.ModelSerializer):
    """
    Serializer for view MonthDataList
    Handles creation of Product(s) as well.
    """
    # products = MonthDataProductsField(many=True, read_only=True)
    products = MonthDataProductsField(many=True)

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = MonthData
        fields = [
            'id', 'month', 'products', 'user',
            'starting_modal', 'cashout', 'profit_balance'
        ]
        validators = [
            UniqueForDateValidator(
                queryset=MonthData.objects.all(),
                field='user',
                date_field='month',
                message='Month with the same user already exists.'
            )
        ]

    def validate_month(self, value):
        if value.day != 1:
            raise serializers.ValidationError("Month must not be any other date than 1st.")
        return value

class MonthDataSerializer(serializers.ModelSerializer):
    products = MonthDataProductsField(many=True, read_only=True)
    sales = SaleSerializer(many=True, read_only=True)
    purchases = PurchaseSerializer(many=True, read_only=True)
    expenses = ExpenseSerializer(many=True, read_only=True)
    previous_balances = PreviousBalanceSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = MonthData
        fields = [
            'id', 'month', 'products', 'sales', 'expenses',
            'purchases', 'previous_balances', 'user',
            'starting_modal', 'cashout', 'profit_balance'
        ]
        validators = [
            UniqueForDateValidator(
                queryset=MonthData.objects.all(),
                field='user',
                date_field='month',
                message='Month with the same user already exists.'
            )
        ]

    def validate_month(self, value):
        if value.day != 1:
            raise serializers.ValidationError("Month must not be any other date than 1st.")
        return value
