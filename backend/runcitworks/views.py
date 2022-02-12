
from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from django.db.models import ProtectedError
from django.db import IntegrityError

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .permissions import  IsOwnerOrReadOnly, SaleIsOwner
from .models import Expense, PreviousBalance, Sale, Purchase, MonthData, Product
from .serializers import ExpenseSerializer, MonthDataListSerializer, ProductSerializer, SaleSerializer, PurchaseSerializer, MonthDataSerializer, PreviousBalanceSerializer, MonthDataPatchSerializer

class MonthDataProduct(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, pk):
        """
        View for adding product to monthdata.
        Essentially this view tries to get a Product object
        and then add it to the monthdata(of <int:pk>).
        Does additonal checks here and there to make sure it's consistent.
        """
        # get the monthdata
        monthdata = get_object_or_404(MonthData, pk=pk)

        self.check_object_permissions(request, monthdata)

        # get the product
        data = request.data.get('name')
        try:
            product = Product.objects.get(user=request.user, name=data)
        except Product.DoesNotExist:
            return Response(
                {'product': 'Product does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # check if product already exists
        if product in monthdata.products.all():
            return Response(
                {'product': f'Product {product.name} already exist within this month.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # apply ManyToMany relation
        monthdata.products.add(product)

        # save monthdata
        monthdata.save()

        # return 200
        serializer = MonthDataSerializer(monthdata)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except IntegrityError:
            return Response(
                {"detail": f"Product '{serializer.data['name']}' already exists for user '{self.request.user.username}'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

# for deleting Product objects
class ProductDetail(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            res = {
                'detail': 'Unable to delete product. Delete all Sales/Products'
                          '/Previous Balances tied to this product before trying.'
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

class SaleList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, SaleIsOwner]
    serializer_class = SaleSerializer

    def get_queryset(self):
        queryset = Sale.objects.filter(account__owner=self.request.user)
        account = self.request.query_params.get('account')
        if account is not None:
            try:
                int(account)
            except ValueError:
                raise Http404('Invalid Parameter.')
            queryset = queryset.filter(account=account)
        return queryset

class SaleDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, SaleIsOwner]
    serializer_class = SaleSerializer

    def get_queryset(self):
        return Sale.objects.all()

class PurchaseList(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, SaleIsOwner]
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return Purchase.objects.all()

class PurchaseDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, SaleIsOwner]
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return Purchase.objects.all()

class ExpenseList(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, SaleIsOwner]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.all()

class ExpenseDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, SaleIsOwner]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.all()

class PreviousBalanceList(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, SaleIsOwner]
    serializer_class = PreviousBalanceSerializer

    def get_queryset(self):
        return PreviousBalance.objects.all()

class PreviousBalanceDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, SaleIsOwner]
    serializer_class = PreviousBalanceSerializer

    def get_queryset(self):
        return PreviousBalance.objects.all()

class MonthDataList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = MonthDataListSerializer

    def get_queryset(self):
        return MonthData.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MonthDataDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = MonthDataSerializer

    def get_queryset(self):
        return MonthData.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Using a different serializer here because of
        # UniqueMonthValidator requiring user and month be always present.
        # MonthDataPatchSerializer does not allow `user` and `month` to be changed,
        # so there is(fingers crossed) no concern with modifying user/month here.
        serializer = MonthDataPatchSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
