from django.db import models
from django.contrib.auth.models import User
# (https://stackoverflow.com/questions/63771879/visual-studio-code-django-error-when-importing-user-model)

# Create your models here.


class Account(models.Model):
    # AutoField for ID
    username = models.CharField(max_length=50)
    hutang = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    owner = models.ForeignKey(
        User, related_name='accounts', on_delete=models.CASCADE, editable=False
    )
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# HistoryStack
#   is a change of hutang
#   for 1 account which belongs to 1 owner


class HistoryStack(models.Model):
    # account_owner = models.ForeignKey(User, related_name='')
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    account = models.ForeignKey(
        Account, related_name='history', on_delete=models.CASCADE, editable=False
    )
    mutation = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['-date_created']
