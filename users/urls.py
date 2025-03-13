from django.urls import path
from . import views


urlpatterns = [
   path('profile/<str:id>', views.profile, name='profile'),
   path('profile/settings/',views.profileSettings, name='settings'),


   path('login/', views.loginPage, name='login'),
   path('logout/',views.logoutUser, name='logout'),
   path('register/', views.registerUser, name='register'),

   path('explore/', views.explore, name='explore'),
]
