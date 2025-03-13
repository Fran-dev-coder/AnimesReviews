from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('anime/<str:id>/', views.anime_detail, name='anime_detail'),

    path('delete-review/<str:id>/', views.deleteReview, name='delete_review'),

]
