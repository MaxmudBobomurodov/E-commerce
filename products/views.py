from django.contrib.admin.templatetags.admin_list import pagination
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django_filters.rest_framework import DjangoFilterBackend
from requests import delete
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from unicodedata import category

from products.filters import ProductFilter
from products.models import Product, Category
from products.serializers import ProductSerializer, CategorySerializer
from shared.utils.custom_response import CustomResponse



class GetCategoryAPIView(APIView):
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


    def get_permissions(self):
        if self.request.method=='GET':
            return [AllowAny(),]
        return [IsAuthenticated(), IsAdminUser()]


    def get(self,request):
        category = Category.objects.all()
        paginator = PageNumberPagination()

        result_page = paginator.paginate_queryset(category, request=request)

        serializer = self.serializer_class(result_page, many=True)

        return CustomResponse.success(
            message_key="SUCCESS",
            data={
                "count":paginator.page.paginator.count,
                "next":paginator.get_next_link(),
                "previous":paginator.get_previous_link(),
                "results": serializer.data,
            },
            request=request
        )

    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(
                message_key="SUCCESS",
                data=serializer.data,
                request=request
            )

    def put(self,request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(message_key="SUCCESS", data=serializer.data, request=request)

    def patch(self,request,pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(message_key="SUCCESS",data=serializer.data,request=request)


    def delete(self,request,pk=None):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return CustomResponse.success(message_key="SUCCESS",request=request)

class GetProductsAPIView(APIView):


    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.request.method=='GET':
            return [AllowAny(),]
        return [IsAuthenticated(), IsAdminUser()]


    def get(self,request):
        products = Product.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(products, request)

        serializer = self.serializer_class(result_page, many=True)


        return CustomResponse.success(
            message_key='SUCCESS',
            data={
                "count":paginator.page.paginator.count,
                "next":paginator.get_next_link(),
                "previous":paginator.get_previous_link(),
                "results": serializer.data,
            },
            request=request
            )
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(created_by=request.user)
            return CustomResponse.success(
                message_key='SUCCESS',
                data=serializer.data,
                request=request
            )
    def put(self,request, pk=None):
        product = Product.objects.get(pk=pk)
        serializer = self.serializer_class(product, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(
                message_key='SUCCESS',
                data=serializer.data,
                request=request
            )
    def patch(self,request,pk=None):
        product = Product.objects.get(pk=pk)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return CustomResponse.success(
                message_key='SUCCESS',
                data=serializer.data,
                request=request
            )
    def delete(self,request,pk=None):
        product = Product.objects.get(pk=pk)
        product.delete()
        return CustomResponse.success(
            message_key='SUCCESS',
            data={'id':pk},
            request=request
        )



# class GetPaginate(GenericAPIView):
#
#     serializer_class = ProductSerializer
#     pagination_class = PageNumberPagination
#
#     def get_permissions(self):
#         if self.request.method=='GET':
#             return [AllowAny(),]
#         return [IsAuthenticated(), IsAdminUser()]
#
#
#     def get(self,request):
#         products = Product.objects.all()
#
#
#         page = self.paginate_queryset(products)
#         if page is not None:
#             serializer = self.serializer_class(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.serializer_class(products, many=True)
#
#         return CustomResponse.success(
#             message_key='SUCCESS',
#             data=serializer.data,
#             request=request
#             )



class ProductFilterAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name']