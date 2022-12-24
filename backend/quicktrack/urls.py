from django.urls import path
from django.urls.conf import re_path
from django.views.generic.base import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns

from quicktrack import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    #     path('registerSW.js', (TemplateView.as_view(template_name="registerSW.js",
    #     content_type='application/javascript', )), name='sw.js'),
    #     path('sw.js', (TemplateView.as_view(template_name="sw.js",
    #     content_type='application/javascript', )), name='sw.js'),

    #     path('manifest.webmanifest', (TemplateView.as_view(template_name="manifest.webmanifest",
    # content_type='application/json', )), name='manifest'),

    path('api/admin/curruser', views.GetCurrUser.as_view()),
    path('api/accounts', views.AccountList.as_view()),
    path('api/accounts/<int:pk>', views.AccountDetail.as_view()),
    path('api/accounts/<int:pk>/merge', views.AccountMerge.as_view()),
    path('api/accounts/<int:pk>/sales', views.AccountSale.as_view()),
    path('api/accounts/<int:pk>/history', views.ListAccountHistory.as_view()),

    # fallback path
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
