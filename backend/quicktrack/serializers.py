from datetime import datetime, timedelta

from rest_framework import serializers

from runcitworks.serializers import SaleSerializer

from .models import Account
from .models import HistoryStack


class HistoryStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryStack
        fields = ['date_created', 'account', 'mutation']
        # read_only_fields = ['date_created']


class AccountSerializer(serializers.ModelSerializer):
    hutang = serializers.DecimalField(
        decimal_places=2, max_digits=6, default=0)
    # history = HistoryStackSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'username', 'hutang', 'owner', 'hidden']


class AccountSaleSerializer(serializers.ModelSerializer):
    """Serializes sales associated with specific account."""
    recent_sales = serializers.SerializerMethodField(
        method_name='get_recent_sales')

    class Meta:
        model = Account
        fields = ['id', 'username', 'hutang',
                  'owner', 'hidden', 'recent_sales']

    def get_recent_sales(self, obj):
        fourty_days_delta = timedelta(40)
        today = datetime.today()
        fourty_days_ago = today - fourty_days_delta

        return SaleSerializer(obj.sales.all().filter(date__gte=fourty_days_ago.date()), many=True).data
