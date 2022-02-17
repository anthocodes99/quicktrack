import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from quicktrack import models as qtmodel

# Create your models here.


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} owned by {self.user.username}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'user'], name='unique product name for every user')
        ]


class MonthData(models.Model):
    """
    Stores all information of the month
    products, user, starting modal, cashout, profit_balance
    sales, purchases and previous balances
    This monthdata will be the only model required for all datapoints
    """
    month = models.DateField()
    products = models.ManyToManyField(Product, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, unique_for_date='month')

    starting_modal = models.DecimalField(
        default=0, max_digits=12, decimal_places=4)
    cashout = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    profit_balance = models.DecimalField(
        default=0, max_digits=12, decimal_places=4)

    def __str__(self):
        return (f'{self.month.month} / {self.month.year} -- {self.user.username}')

    def clean(self):
        for product in self.products.all():
            if product.user != self.user:
                raise ValidationError(
                    _(f'Product {product} must be from the same user {self.user}.'))

    class Meta:
        ordering = ['-month']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'month'], name='1 month per user only.')
        ]


class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monthdata = models.ForeignKey(
        MonthData, related_name='sales', on_delete=models.CASCADE)
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.DecimalField(default=0, max_digits=9, decimal_places=4)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MaxValueValidator(10000000)])
    account = models.ForeignKey(
        qtmodel.Account, related_name='sales', on_delete=models.SET_NULL, null=True, blank=True)

    def get_monthdata(self):
        return self.monthdata

    def clean(self):
        if self.product not in self.monthdata.products.all():
            raise ValidationError(
                _('Product should be registered in MonthData.'))

        if self.date.month != self.monthdata.month.month:
            raise ValidationError(
                _('Date for sale can only be within the current month.'))


class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monthdata = models.ForeignKey(
        MonthData, related_name='purchases', on_delete=models.CASCADE)
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.DecimalField(default=0, max_digits=9, decimal_places=4)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MaxValueValidator(10000000)])

    def get_monthdata(self):
        return self.monthdata

    def clean(self):
        if self.product not in self.monthdata.products.all():
            raise ValidationError(
                _('Product should be registered in MonthData.'))

        if self.date.month != self.monthdata.month.month:
            raise ValidationError(
                _('Date for sale can only be within the current month.'))


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monthdata = models.ForeignKey(
        MonthData, related_name='expenses', on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=128)
    unit_price = models.DecimalField(default=0, max_digits=9, decimal_places=4)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MaxValueValidator(10000000)])
    # trying something new; snapshot of when the object is created.
    # to be implemented on purchase and sales
    created = models.DateTimeField(auto_now_add=True)

    def get_monthdata(self):
        return self.monthdata

    def clean(self):
        if self.date.month != self.monthdata.month.month:
            raise ValidationError(
                _('Date for expense can only be within the current month.'))


class PreviousBalance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monthdata = models.ForeignKey(
        MonthData, related_name='previous_balances', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.DecimalField(default=0, max_digits=9, decimal_places=4)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MaxValueValidator(10000000)])

    def get_monthdata(self):
        return self.monthdata

    def clean(self):
        if self.product not in self.monthdata.products.all():
            raise ValidationError(
                _('Product should be registered in MonthData.'))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'monthdata'], name='No Duplicate Previous Balances')
        ]
