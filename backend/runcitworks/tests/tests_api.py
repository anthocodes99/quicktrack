from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from runcitworks import models
from runcitworks import views

User = get_user_model()

class TestProductViews(TestCase):
    """
    Tests views related to Product:
        ProductList
        ProductDetail

    ProductMonthData will be tested separately.
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='antho', password='bottom_secret'
        )

    def test_product_post(self):
        """
        Checks if Product can be created.
        Checks if Product created matches.
        """
        data = {
            'name': 'apples',
            'user': self.user.id
        }
        request = self.factory.post('/api/v1/products', data)
        force_authenticate(request, user=self.user)
        response = views.ProductList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['user'], data['user'])

    def test_product_post_unique_validator(self):
        """
        Tests if ProductList properly returns 400 if Product already
        exists for current user.
        """
        data = {
            'name': 'apples',
            'user': self.user.id
        }
        init_request = self.factory.post('/api/v1/products', data)
        force_authenticate(init_request, user=self.user)
        init_response = views.ProductList.as_view()(init_request)
        self.assertEqual(init_response.status_code, status.HTTP_201_CREATED)
        dup_request = self.factory.post('/api/v1/products', data)
        force_authenticate(dup_request, user=self.user)
        dup_response = views.ProductList.as_view()(dup_request)
        self.assertEqual(dup_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_detail_get_not_allowed(self):
        """
        Tests ProductDetail making sure that method GET is not allowed.
        """
        request = self.factory.get('/api/v1/products/',)
        force_authenticate(request, user=self.user)
        response = views.ProductDetail.as_view()(request)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['detail'], 'Method "GET" not allowed.')

    def test_product_detail_destroy(self):
        """
        Tests if ProductDetail properly destroys a Product.
        """
        product = models.Product.objects.create(name='asdf', user=self.user)
        request = self.factory.delete(f'/api/v1/products/{product.id}')
        force_authenticate(request, user=self.user)
        response = views.ProductDetail.as_view()(request, pk=product.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_product_detail_destroy_protected(self):
        """
        Tests if ProductDetail properly handles Product which are tied to
        sales.
        """
        product = models.Product.objects.create(name='asdf', user=self.user)
        monthdata = models.MonthData.objects.create(
            month=date(2021, 6, 1), user=self.user)
        monthdata.products.add(product)
        monthdata.save()
        sale_data = {
            'date': date(2021, 6, 5),
            'monthdata': monthdata,
            'product': product,
            'unit_price': 3.0,
            'quantity': 10,
        }
        sale = models.Sale.objects.create(**sale_data)
        request = self.factory.delete(f'/api/v1/products/{product.id}',)
        force_authenticate(request, user=self.user)
        response = views.ProductDetail.as_view()(request, pk=product.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'],
                         'Unable to delete product. Delete all Sales/Products'
                         '/Previous Balances tied to this product before trying.')


class TestSaleViews(TestCase):
    """
    Test views related to Sale:
        SaleList
        SaleDetail
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='antho', password='bottom_secret'
        )
        self.monthdata = models.MonthData.objects.create(
            month=date(2021, 6, 1), user=self.user
        )
        self.product = models.Product.objects.create(
            name='Apples', user=self.user
        )
        self.monthdata.products.add(self.product)

    def test_sale_post(self):
        """
        Tests if Sale can be created.
        Tests if Sale created matches.
        """
        sale_data = {
            'date': date(2021, 6, 5),
            'monthdata': self.monthdata.id,
            'product': self.product.name,
            'unit_price': 3.0,
            'quantity': 10,
        }
        request = self.factory.post('/api/v1/sale', sale_data)
        force_authenticate(request, user=self.user)
        response = views.SaleList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['date'], '2021-06-05')
        self.assertEqual(response.data['monthdata'], 1)
        self.assertEqual(response.data['product'], 'Apples')
        self.assertEqual(response.data['unit_price'], '3.0000')
        self.assertEqual(response.data['quantity'], 10)

    def test_sale_product_from_different_user(self):
        """
        Tests if Sale rejects creation if Sale user mismatches.
        """
        mis_user = User.objects.create_user(
            username='antho2', password='left_secret'
        )
        # The way how the code should work is that this should not be
        # test-able as you shouldn't be able to register a monthdata
        # product that is from another user.
        pass

    def test_sale_product_not_in_monthdata(self):
        """
        Tests if Sale rejects creation if Product is not in Monthdata.
        """
        mis_product = models.Product.objects.create(
            name='Grapes', user=self.user)
        sale_data = {
            'date': date(2021, 6, 5),
            'monthdata': self.monthdata.id,
            'product': mis_product.name,
        }
        request = self.factory.post('/api/v1/sale', sale_data)
        force_authenticate(request, user=self.user)
        response = views.SaleList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        detail = "Invalid product.\'Grapes\' does not exist within this month."
        self.assertEqual(str(response.data['product']), detail)

    def test_sale_quantity_overflow(self):
        """
        Tests if Sale correctly handles OverflowError if given a large input of
        numbers for quantity.
        """
        sale_data = {
            'date': date(2021, 6, 5),
            'monthdata': self.monthdata.id,
            'product': self.product.name,
            'quantity': 9223372036854775800000,  # 64 bit signed integer + 4 zeros
        }
        request = self.factory.post('/api/v1/sale', sale_data)
        force_authenticate(request, user=self.user)
        response = views.SaleList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        detail = "Ensure this value is less than or equal to 10000000."
        self.assertEqual(str(response.data['quantity'][0]), detail)

    def test_sale_unit_price_decimals(self):
        """
        Tests if unit price returns up to 4 decimals place
        """
        sale_data = {
            'date': date(2021, 6, 5),
            'monthdata': self.monthdata.id,
            'product': self.product.name,
            'quantity': 10000000,  # 10mil cus why not.
            'unit_price': 1.0001
        }
        request = self.factory.post('/api/v1/sale', sale_data)
        force_authenticate(request, user=self.user)
        response = views.SaleList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['unit_price'], "1.0001")

    def test_sale_unit_price_decimals_over_limit(self):
        """
        Tests response if unit price is given more than 4 decimal places
        """
        sale_data = {
            'date': date(2021, 6, 5),
            'monthdata': self.monthdata.id,
            'product': self.product.name,
            'quantity': 10000000,  # 10mil cus why not.
            'unit_price': 1.00001  # 5 decimal....places???!!!
        }
        request = self.factory.post('/api/v1/sale', sale_data)
        force_authenticate(request, user=self.user)
        response = views.SaleList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        detail = 'Ensure that there are no more than 4 decimal places.'
        self.assertEqual(str(response.data['unit_price'][0]), detail)

    def test_sale_unit_price_digits_over_limit(self):
        """
        Tests response if unit price is given more than 9 digits
        """
        sale_data = {
            'date': date(2021, 6, 5),
            'monthdata': self.monthdata.id,
            'product': self.product.name,
            'quantity': 10000000,  # 10mil cus why not.
            'unit_price': 123456.0001  # 10....digits???!!!
        }
        request = self.factory.post('/api/v1/sale', sale_data, format='json')
        force_authenticate(request, user=self.user)
        response = views.SaleList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        detail = 'Ensure that there are no more than 9 digits in total.'
        self.assertEqual(str(response.data['unit_price'][0]), detail)

    def test_sale_monthdata_date_mismatch(self):
        """
        Tests Sale response if date and monthdata's month mismatches.
        """
        sale_data = {
            'date': date(2021, 7, 5),
            'monthdata': self.monthdata.id,  # this is on june
            'product': self.product.name,
            'quantity': 10000000,  # 10mil cus why not.
            'unit_price': 12345.6789  # maxing the capabiltiies
        }
        request = self.factory.post('/api/v1/sale', sale_data)
        force_authenticate(request, user=self.user)
        response = views.SaleList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        detail = 'Date for sale can only be within the current month.'
        self.assertEqual(str(response.data['date'][0]), detail)

class TestMonthDataViews(TestCase):
    """
    Test any views related to MonthData:
        MonthDataList
        MonthDataDetail
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='antho', password='bottom_secret'
        )

    def test_monthdata_create(self):
        """
        Tests if MonthData can be created.
        Tests if MonthData created matches.
        """
        monthdata = {
            'month': date(2021, 6, 1),
            'cashout': 10,
            'profit_balance': 0.1114
        }
        request = self.factory.post('/api/v1/monthdatas', monthdata)
        force_authenticate(request, user=self.user)
        response = views.MonthDataList.as_view()(request)
        self.assertEqual(response.data['month'], '2021-06-01')
        self.assertEqual(response.data['cashout'], '10.0000')
        self.assertEqual(response.data['profit_balance'], '0.1114')
        self.assertEqual(response.data['user'], self.user.id)
    
    def test_monthdata_date_not_first(self):
        """
        Tests if MonthData rejects creation with date not on 1st
        """
        monthdata = {
            'month': date(2021, 6, 2)
        }
        request = self.factory.post('/api/v1/monthdatas', monthdata)
        force_authenticate(request, user=self.user)
        response = views.MonthDataList.as_view()(request)
        # print(f'{response.data=}')
        detail = 'Month must not be any other date than 1st.'
        self.assertEqual(str(response.data['month'][0]), detail)

    def test_monthdata_month_already_exists(self):
        """
        Tests if MonthData rejects creation with the same month.
        """
        monthdata = {
            'month': date(2021, 6, 1)
        }
        # testing if the first monthdata is created properly
        request = self.factory.post('/api/v1/monthdatas', monthdata)
        force_authenticate(request, user=self.user)
        response = views.MonthDataList.as_view()(request)
        # should return 201 if created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create another monthdata with the same inputs
        request = self.factory.post('/api/v1/monthdatas', monthdata)
        force_authenticate(request, user=self.user)
        response = views.MonthDataList.as_view()(request)
        print(f'{response.data=}')
        detail = 'Month with the same user already exists.'
        self.assertEqual(str(response.data['user'][0]), detail)

    def test_monthdata_ignores_user_id(self):
        """
        Tests if monthdata ignores user id.
        """
        dummy_user = User.objects.create_user(
            username='antho2', password='left_secret')
        monthdata = {
            'month': date(2021, 6, 1),
            'user': dummy_user.id # polluting the data
        }
        request = self.factory.post('/api/v1/monthdatas', monthdata)
        force_authenticate(request, user=self.user)
        response = views.MonthDataList.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], 1)

    def test_monthdata_patch(self):
        """
        Tests if MonthData is successfully edited through PATCH
        """
        pass

class MonthDataProductTest(TestCase):
    """
    Testing the view MonthDataProduct
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='antho', password='bottom_secret'
        )
        self.monthdata = models.MonthData.objects.create(
            month=date(2021, 6, 1), user=self.user
        )
        self.product = models.Product.objects.create(
            name='Apples', user=self.user
        )

    def test_product_add(self):
        """
        Tests if MonthDataProduct adds Product to MonthData properly.
        """
        pass

    def test_product_already_exists(self):
        """
        Tests if MonthDataProduct rejects adding Product that already exists.
        More accurately, returns 400(it has not implication on backend)
        """
        pass
    
    def test_product_not_exist(self):
        """
        Tests if MonthDataProduct rejects adding Product that doesn't exist.
        It can't anyways. Should return 401
        """
        pass

    def test_data_pollution(self):
        """
        What if.....I put 2 names?
        """
        pass
