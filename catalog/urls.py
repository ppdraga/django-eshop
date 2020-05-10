from django.urls import path

from catalog.views import GoodItemListView, GoodItemCreateView

urlpatterns = [
    path('', GoodItemListView.as_view(), name='catalog'),
    path('product/add/', GoodItemCreateView.as_view(), name='product-add'),
]

