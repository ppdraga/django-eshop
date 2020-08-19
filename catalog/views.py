from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from rest_framework.decorators import api_view, action
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status, mixins, generics, viewsets

from catalog.serializers import GoodItemSerializer
from catalog.models import GoodItem
from catalog.forms import GoodItemForm

# Create your views here.

class GoodItemListView(ListView):
    model = GoodItem
    template_name = 'catalog/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return GoodItem.objects.all()

class GoodItemDetailView(DetailView):
    model = GoodItem

class GoodItemCreateView(CreateView):
    model = GoodItem
    fields = ['title', 'vendor', 'price', 'unit_of_measure']
    success_url = '/'

class GoodItemUpdateView(UpdateView):
    model = GoodItem

class GoodItemDeleteView(DeleteView):
    model = GoodItem

def add(request):
    data = dict()
    if request.method == 'POST':
        form = GoodItemForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            products = GoodItem.objects.all()
            data['products_html'] = render_to_string('catalog/list.html', {'products': products})
        else:
            data['form_html'] = render_to_string('catalog/gooditem_modal_form.html', {'form': form}, request=request)

    else:
        data['form_is_valid'] = False
        data['form_html'] = render_to_string('catalog/gooditem_modal_form.html', {'form': GoodItemForm()}, request=request)

    return JsonResponse(data)


# DRF Views

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('catalog:user-list', request=request, format=format),
        'products': reverse('catalog:product-list', request=request, format=format)
    })

#######################
# func-based drf views:
#######################

# @api_view(['GET', 'POST'])
# def product_list(request, format=None):
#     """
#     List all goods, or create a new good.
#     """
#     if request.method == 'GET':
#         products = GoodItem.objects.all()
#         serializer = GoodItemSerializer(products, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = GoodItemSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a product.
#     """
#     try:
#         product = GoodItem.objects.get(pk=pk)
#     except GoodItem.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = GoodItemSerializer(product)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = GoodItemSerializer(product, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         product.delete()
#         return HttpResponse(status=204)


###################
# class-based views
###################

# class ProductList(APIView):
#     """
#     List all products, or create a new product.
#     """
#     def get(self, request, format=None):
#         products = GoodItem.objects.all()
#         serializer = GoodItemSerializer(products, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = GoodItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ProductDetail(APIView):
#     """
#     Retrieve, update or delete a product instance.
#     """
#     def get_object(self, pk):
#         try:
#             return GoodItem.objects.get(pk=pk)
#         except GoodItem.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         product = self.get_object(pk)
#         serializer = GoodItemSerializer(product)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         product = self.get_object(pk)
#         serializer = GoodItemSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         product = self.get_object(pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


###############################
# class-based views with mixins
###############################

# class ProductList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = GoodItem.objects.all()
#     serializer_class = GoodItemSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ProductDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = GoodItem.objects.all()
#     serializer_class = GoodItemSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

###############################
# class-based generic drf views
###############################

class ProductList(generics.ListCreateAPIView):
    queryset = GoodItem.objects.all()
    serializer_class = GoodItemSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GoodItem.objects.all()
    serializer_class = GoodItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = GoodItem.objects.all()
    serializer_class = GoodItemSerializer
