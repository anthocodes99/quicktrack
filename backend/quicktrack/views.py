import logging

from django.shortcuts import render, get_object_or_404

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from runcitworks.serializers import SaleSerializer
from runcitworks.models import Sale

from .models import Account, HistoryStack
from .permissions import IsOwner, AccountSaleIsOwner
from .serializers import AccountSerializer, HistoryStackSerializer

logger = logging.getLogger(__name__)

# Create your views here.

# rest framework stuffs


class AccountSale(generics.ListCreateAPIView):
    """
    If you're still seeing this then PLEASE TELL the developer
    to FIX HIS CRAPPY CODE because there's a lot to be
    EXPLOITED on this endpoint
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, AccountSaleIsOwner]
    serializer_class = SaleSerializer

    def get_queryset(self):
        """
        Please dont do this madness
        Obtains a list of Sales from <int:pk> of account
        using Sale.objects.filter(account=pk)
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        account = get_object_or_404(Account, pk=self.kwargs[lookup_url_kwarg])
        # Check if the user has permission to the Account object
        qs = Sale.objects.filter(account=account)
        self.check_object_permissions(self.request, obj=qs[0])
        return qs

    def perform_create(self, serializer):
        """
        Some issues:
        You can still POST to unknown Account IDs although
        it returns "Not Found"
        LMAO seems like you can POST to wrong accounts
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        # Needed to prevent people from assigning to other accounts
        # This was the easiest
        account = get_object_or_404(Account, pk=self.kwargs[lookup_url_kwarg])
        if account.owner != self.request.user:
            self.permission_denied(self.request)
        serializer.save(account=account)
        amount = serializer.validated_data['unit_price'] * \
            serializer.validated_data['quantity']
        account.hutang += amount
        account.save()
        # print(f'SaleAccount/perform_create() -- amount : {amount}')


class GetCurrUser(APIView):
    """
    (Temporary) Admin tool for requesting current user.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            # `django.contrib.auth.User` instance.
            'user': request.user.username,
            'auth': request.auth,  # None
        }
        return Response(content)


class AccountList(generics.ListCreateAPIView):
    """
    GET - Lists all accounts that belongs to the current user.
    POST - Creates a new account that belongs to the current user.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get_queryset(self):
        return self.request.user.accounts.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def update(self, request, *args, **kwargs):
        """
        Modified to send a mutation along the response for frontend.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # !! MODIFICATION !!
        # self.perform_update for this view returns history
        history = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # same thing here ; only changes towards hutang creates a mutation
        if history is not None:
            history_serializer = HistoryStackSerializer(history)
            data = {**serializer.data, 'mutation': {**history_serializer.data}}
        else:
            data = {**serializer.data}
        return Response(data)

    def perform_update(self, serializer):
        """
        !! Modified !!
        Creates a HistoryStack mutation object based on the difference in hutang.\n
        Returns a `HistoryStack` object.
        """
        # print(serializer.validated_data)
        history = None
        # only perform update when PATCH includes 'hutang' as a field
        if serializer.validated_data.get('hutang', None) is not None:
            # serializer's instance is account's detail current view(pk)
            account = serializer.instance
            prev_hutang = account.hutang  # instance's hutang before .save()
            diff = serializer.validated_data['hutang'] - prev_hutang
            # print('prev_hutang: ', prev_hutang, '| diff: ', diff)
            history = HistoryStack.objects.create(
                account=account, mutation=diff)
            history.save()  # creates a mutation
        serializer.save()
        return history


class AccountMerge(APIView):
    """
    POST - Merges current account to another account
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, pk, format=None):
        """
        Merges current account to another account
        """
        # Get current account
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            # we do not use get_object_or_404
            # because we need to control the response
            return Response({'detail': 'Current account does not exist'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, account)

        # get target account
        data = request.data.get('account')
        try:
            target_account = Account.objects.get(pk=data)
        except Account.DoesNotExist:
            return Response({'detail': 'Target account does not exist'}, status.HTTP_404_NOT_FOUND)

        if account == target_account:
            return Response({'detail': 'Target account is the current account'}, status.HTTP_400_BAD_REQUEST)

        # get all sales from current account
        qs = Sale.objects.filter(account=account)
        # make sure target account is also owned by current user
        self.check_object_permissions(request, target_account)

        # change account to target account
        for query in qs:
            query.account = target_account
            query.save()

        # return 201 created
        return Response({'detail': 'Successfully merged account.'}, status=status.HTTP_201_CREATED)


class ListAccountHistory(APIView):
    """
    GET - Lists a single account's hutang dispatch history.
    POST - Dispatches a commit for an account's hutang.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, pk, format=None):
        """
        Return a list of history for an account.
        """
        account = Account.objects.get(pk=pk)
        self.check_object_permissions(request, account)
        history = HistoryStack.objects.filter(account=account)
        serializer = HistoryStackSerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
