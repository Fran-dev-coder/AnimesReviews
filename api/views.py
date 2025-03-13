from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import AnimeSerializer, ReviewSerializer, CategorySerializer, ProfileSerializer
from reviews.models import Anime, Review, Category
from users.models import Profile

@api_view(['GET'])
def getRoutes(request):
    
    routes = [
        {'GET': 'api/animes'},
        {'GET': 'api/animes/id'},

        {'POST': 'api/users/token'},
        {'POST': 'api/users/token/refresh'},
    ]

    return Response(routes)

@api_view(['GET'])
def getAnimes(request):
    animes = Anime.objects.all()
    serializer = AnimeSerializer(animes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAnime(request,id):
    anime = Anime.objects.get(id=id)
    serializer = AnimeSerializer(anime, many=False)
    return Response(serializer.data)



@api_view(['GET'])
def getReviews(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getReview(request,id):
    review = Review.objects.get(id=id)
    serializer = ReviewSerializer(review, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCategory(request,id):
    category = Category.objects.get(id=id)
    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getProfiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProfile(request,id):
    profile = Profile.objects.get(id=id)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rateAnime(request,id):
    anime = Anime.objects.get(id=id)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner = user,
        anime = anime,
        defaults={'rating': data['rating']} 
    )
    if not created:
        review.rating = data['rating']
        review.save()
    
    serializer = AnimeSerializer(anime, many=False)
    return Response(serializer.data)

