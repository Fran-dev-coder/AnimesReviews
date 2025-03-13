from rest_framework import serializers
from reviews.models import Anime, Review, Category
from users.models import Profile

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    class Meta:
        model = Review
        fields = '__all__'

class AnimeSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Anime
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

