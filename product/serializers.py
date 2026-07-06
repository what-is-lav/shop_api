from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = 'id name products_count'.split()



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = 'id title description price category reviews rating'.split()

    def get_rating(self, product):
        return round(product.rating, 2) if product.rating else 0


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2, max_length=255)


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2, max_length=255)
    description = serializers.CharField(required=False, default="No description")
    price = serializers.FloatField(min_value=0.01)
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category not found!')
        return category_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=5)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product not found!')
        return product_id