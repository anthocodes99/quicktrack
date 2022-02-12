from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from runcitworks import views

urlpatterns = [
    path('api/v1/sales', views.SaleList.as_view()),
    path('api/v1/sales/<str:pk>', views.SaleDetail.as_view()),
    path('api/v1/purchases', views.PurchaseList.as_view()),
    path('api/v1/purchases/<str:pk>', views.PurchaseDetail.as_view()),
    path('api/v1/expenses', views.ExpenseList.as_view()),
    path('api/v1/expenses/<str:pk>', views.ExpenseDetail.as_view()),
    path('api/v1/previousbalances', views.PreviousBalanceList.as_view()),
    path('api/v1/previousbalances/<str:pk>', views.PreviousBalanceDetail.as_view()),
    path('api/v1/products', views.ProductList.as_view()),
    path('api/v1/products/<str:pk>', views.ProductDetail.as_view()),
    path('api/v1/monthdatas', views.MonthDataList.as_view()),
    path('api/v1/monthdatas/<int:pk>', views.MonthDataDetail.as_view()),
    path('api/v1/monthdatas/<int:pk>/products', views.MonthDataProduct.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
