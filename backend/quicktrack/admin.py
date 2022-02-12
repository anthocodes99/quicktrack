from django.contrib import admin

# Register your models here.
from .models import Account

# wtf did i do
# why did i set account's owner to be non-editable???

@admin.action(description='Mark selected accounts as hidden')
def make_hidden(modeladmin, request, queryset):
    queryset.update(hidden=True)

@admin.action(description='Mark selected accounts as not hidden')
def make_unhidden(modeladmin, request, queryset):
    queryset.update(hidden=False)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'owner', 'hidden']
    fields = ('username', 'hutang', 'hidden')
    actions = [make_hidden, make_unhidden]
