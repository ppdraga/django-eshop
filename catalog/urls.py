from django.urls import path

from catalog.views import GoodItemListView, GoodItemCreateView, add
# from catalog.views import product_detail, product_list
from catalog.views import ProductList, ProductDetail

app_name = 'catalog'

urlpatterns = [
    path('', GoodItemListView.as_view(), name='index'),
    # path('product/add/', GoodItemCreateView.as_view(), name='product-add'),
    path('product/add', add, name='product-add'),
    # path('product/api/', product_list),
    # path('product/api/<int:pk>/', product_detail),
    path('product/api/', ProductList.as_view()),
    path('product/api/<int:pk>/', ProductDetail.as_view()),
]

import rest_framework.urlpatterns as drf_urlpatterns
urlpatterns = drf_urlpatterns.format_suffix_patterns(urlpatterns)
