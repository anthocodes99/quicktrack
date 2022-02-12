from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from runcitworks import models
from runcitworks import views

User = get_user_model()

class MonthDataTest(TestCase):

    def test_clean(self):
        """
        Test if clean correctly detects product from a different user.
        I'm going to explain some things here :
            models.clean() is not called by:
                rest_framework Generic Views (checks is on serializer)
                models.create()[which is models.save() behind the scenes]
                models.save()
            it is however called by:
                admin sites
                form views(is_valid())
        """
        def action():
            user = User.objects.create_user('antho', '', '')
            user2 = User.objects.create_user('antho2', '', '')
            product = models.Product.objects.create(name='Apple', user=user2)
            date_data = date(2021, 6, 1)
            monthdata = models.MonthData.objects.create(
                month=date_data, user=user)
            monthdata.products.add(product)
            monthdata.clean()  # I'm intentially calling clean here to test
            monthdata.save()  # this specific case
        self.assertRaises(ValidationError, action)
