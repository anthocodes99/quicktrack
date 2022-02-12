from django.conf.urls import url
from django.urls import path
from django.urls.conf import re_path
from django.views.generic.base import TemplateView

from rest_framework.urlpatterns import format_suffix_patterns

from quicktrack import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('service-worker.js', (TemplateView.as_view(template_name="service-worker.js", content_type='application/javascript', )), name='sw.js'),

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
