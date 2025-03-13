from django.contrib.auth.models import User
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q
from .models import Anime

def get_user_profile(user):
    if user.is_authenticated:
        return user.profile 
    return None


def average_stars(rating):
    full_stars = int(rating)
    half_star = (rating - full_stars) >= 0.5
    empty_stars = 5 - full_stars - int(half_star)
    return full_stars, half_star, empty_stars


def paginateAnimes(request,animes,results):
    page = request.GET.get('page')
    paginator = Paginator(animes,results)

    try:
        animes = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        animes = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        animes = paginator.page(page)
    
    leftIndex = (int(page) - 2)

    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 2)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages  + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, animes
    
def searchAnime(request):
    q = ''
    
    if request.GET.get('q'):
        q = request.GET.get('q')
    
    animes = Anime.objects.filter(
        Q(categories__name__icontains=q) |
        Q(title__icontains=q)
    ).distinct()

    return animes,q    