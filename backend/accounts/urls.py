from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (LoginView, logout_view, get_current_user)

urlpatterns = [
    path('accounts/login', LoginView.as_view(), name='login'),
    path('accounts/logout', logout_view),
    path('accounts/me', get_current_user),
]

urlpatterns = format_suffix_patterns(urlpatterns)
