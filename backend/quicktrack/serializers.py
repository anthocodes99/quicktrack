from rest_framework import serializers

from .models import Account
from .models import HistoryStack

class HistoryStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryStack
        fields = ['date_created', 'account', 'mutation']
        # read_only_fields = ['date_created']

class AccountSerializer(serializers.ModelSerializer):
    hutang = serializers.DecimalField(decimal_places=2, max_digits=6, default=0)
    # history = HistoryStackSerializer(many=True, read_only=True)
    class Meta:
        model = Account
        fields = ['id', 'username', 'hutang', 'owner', 'hidden']
