from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Avg

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, ProductSerializer, ReviewSerializer,
    CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer
)

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategorySerializer
    pagination_class = CustomPagination

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        print(request.user)

    def create(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        name = serializer.validated_data.get('name')
        category = Category.objects.create(name=name)
        category_with_count = Category.objects.annotate(products_count=Count('products')).get(id=category.id)
        return Response(status=status.HTTP_201_CREATED, data=CategorySerializer(category_with_count).data)


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        print(request.user)

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        category.name = serializer.validated_data.get('name')
        category.save()
        category_with_count = Category.objects.annotate(products_count=Count('products')).get(id=category.id)
        return Response(status=status.HTTP_200_OK, data=CategorySerializer(category_with_count).data)


class ProductReviewsAPIView(ListAPIView):
    queryset = Product.objects.annotate(rating=Avg('reviews__stars'))
    serializer_class = ProductSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        print(request.user)


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.annotate(rating=Avg('reviews__stars'))
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        print(request.user)

    def create(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        product = Product.objects.create(
            title=serializer.validated_data.get('title'),
            description=serializer.validated_data.get('description'),
            price=serializer.validated_data.get('price'),
            category_id=serializer.validated_data.get('category_id')
        )
        product_with_rating = Product.objects.annotate(rating=Avg('reviews__stars')).get(id=product.id)
        return Response(status=status.HTTP_201_CREATED, data=ProductSerializer(product_with_rating).data)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.annotate(rating=Avg('reviews__stars'))
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        print(request.user)

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        product.save()
        product_with_rating = Product.objects.annotate(rating=Avg('reviews__stars')).get(id=product.id)
        return Response(status=status.HTTP_200_OK, data=ProductSerializer(product_with_rating).data)


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        print(request.user)

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        review = Review.objects.create(
            text=serializer.validated_data.get('text'),
            stars=serializer.validated_data.get('stars'),
            product_id=serializer.validated_data.get('product_id')
        )
        return Response(status=status.HTTP_201_CREATED, data=ReviewSerializer(review).data)


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        print(request.user)

    def update(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')
        review.save()
        return Response(status=status.HTTP_200_OK, data=ReviewSerializer(review).data)