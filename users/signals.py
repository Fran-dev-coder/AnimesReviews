
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile

def createProfile(sender,instance,created,**kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user = user
        )

        subject = 'Welcome to AnimeReviews'
        message =  f"""
        Hello {user.first_name},

        Thank you for joining AnimeReviews! 🎉 We're thrilled to have you in our community of anime enthusiasts.

        Here, you'll find a space where you can discover reviews, share your thoughts, and connect with others who are just as passionate about anime as you are.

        ✨ What to do next?
        - Explore our top-rated reviews.
        - Write your own reviews and share your perspective.
        - Interact with other members and their opinions.

        If you have any questions or feedback, feel free to reach out to us. We're here to make your experience amazing!

        Once again, welcome to the AnimeReviews family. Let’s dive into the anime world together! 🌟

        Warm regards,
        The AnimeReviews Team
        """
        send_mail(
             subject,
             message,
             settings.EMAIL_HOST_USER,
             [user.email],
             fail_silently = False,
        )
def updateUser(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.save()

def deleteUser(sender,instance,**kwargs):
        user = instance.user
        user.delete()

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender = Profile)
post_delete.connect(deleteUser, sender=Profile)