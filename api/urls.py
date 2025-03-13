from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('animes/',views.getAnimes),
    path('anime/<str:id>/',views.getAnime),
    path('anime/<str:id>/rate/',views.rateAnime),

    path('reviews/',views.getReviews),
    path('review/<str:id>/',views.getReview),

    path('categories/',views.getCategories),
    path('category/<str:id>/',views.getCategory),
    
    path('profiles/',views.getProfiles),
    path('profile/<str:id>/',views.getProfile),


]
