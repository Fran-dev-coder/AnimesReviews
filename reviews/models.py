from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

from users.models import Profile
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
class Anime(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='anime_images/',blank=True,null=True)
    categories = models.ManyToManyField(Category)
    release_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(Avg('rating'))['rating__avg'],2)
        return 0
    
    @property
    def review_count(self):
        return self.reviews.count()
    

    
class Review(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name="reviews")
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True,blank=True)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1,6)])
    body_text = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.body_text[0:105]