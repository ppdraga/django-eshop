from django.urls import path, include
from rest_framework.routers import DefaultRouter

from catalog.views import GoodItemListView, GoodItemCreateView, add
# from catalog.views import product_detail, product_list
from catalog.views import ProductList, ProductDetail, ProductViewSet, api_root
from api.views import UserList, UserDetail, UserViewSet

app_name = 'catalog'

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', GoodItemListView.as_view(), name='index'),
    # path('product/add/', GoodItemCreateView.as_view(), name='product-add'),
    path('product/add', add, name='product-add'),
    # path('product/api/', product_list),
    # path('product/api/<int:pk>/', product_detail),
    path('product/api/', ProductList.as_view(), name='product-list'),
    path('product/api/<int:pk>/', ProductDetail.as_view()),
    path('user/api/', UserList.as_view(), name='user-list'),
    path('user/api/<int:pk>/', UserDetail.as_view()),
    # path('api/', api_root),
    # path('api/', include(router.urls)),
]

import rest_framework.urlpatterns as drf_urlpatterns
urlpatterns = drf_urlpatterns.format_suffix_patterns(urlpatterns)

urlpatterns += [path('api/', include(router.urls))]