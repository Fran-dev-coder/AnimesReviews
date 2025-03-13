from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Anime, Review, Category
from .forms import ReviewForm
from .utils import get_user_profile,average_stars, paginateAnimes,searchAnime
from users.models import Profile


# Create your views here.
def home(request):
    animes, q = searchAnime(request)
    custom_range, animes = paginateAnimes(request,animes, 3)

    categories = Category.objects.all()
    anime_count = Anime.objects.all().count()
    
    profile = get_user_profile(request.user)
    
    context = {'categories':categories,'profile':profile,'animes':animes,'anime_count':anime_count,'q':q,'custom_range':custom_range}

    return render(request,'reviews/home.html', context)

def anime_detail(request, id):
    anime = get_object_or_404(Anime, id=id)
    full_stars, half_star, empty_stars = average_stars(anime.average_rating)
    percentage = (anime.average_rating / 5 ) * 100 if anime.average_rating > 0 else 0
    reviews = anime.reviews.all()
    review_user_ids = reviews.values_list('owner__id', flat=True)
    form = ReviewForm()
    
    profile = get_user_profile(request.user)
    is_favorite = profile.favorites.filter(id=anime.id).exists() if profile else False


    if request.method == 'POST':
        if 'submit_review' in request.POST:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.anime = anime
                review.owner = profile
                review.save()
                return redirect('anime_detail', id=id)
            
        if 'favorite' in request.POST:
            if profile:
                if anime not in profile.favorites.all():
                    profile.favorites.add(anime)
                    return redirect('anime_detail', id=id)
                else:
                    profile.favorites.remove(anime)
                    return redirect('anime_detail', id=id)
            else:
                return redirect('login')
            
    context = {'anime':anime,'full_stars':range(full_stars),'half_star':half_star,'empty_stars':range(empty_stars),'percentage':round(percentage,2),'reviews':reviews,'form':form,'review_user_ids':review_user_ids,'is_favorite':is_favorite}
    return render(request,'reviews/anime_detail.html',context)

@login_required(login_url='login')
def deleteReview(request,id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'POST':
        review.delete()
        return redirect('home')
    context = {'obj':review}
    return render(request,'reviews/delete_obj.html',context)