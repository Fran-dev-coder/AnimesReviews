from django.contrib import admin
from .models import Anime, Review, Category
# Register your models here.
admin.site.register(Anime)
admin.site.register(Category)
admin.site.register(Review)
