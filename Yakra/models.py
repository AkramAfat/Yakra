from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


#create tweet model:
class Tweet(models.Model):
    user = models.ForeignKey(
        User, related_name="tweets",
        on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    #added automatically
    likes = models.ManyToManyField(User, related_name="tweet_like" , blank=True)

    #keep track or count of likes
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return(
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )



#create a user profil model / oneto one field = one user can use one profile but manytomany means he can follow many users 
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
         related_name="followed_by",
         symmetrical=False, #not neccessary to follow each other
         blank=True) #don't have to follow anyone


    date_modified = models.DateTimeField(User, auto_now=True) #give use the most stuff and date time field 
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    def __str__(self):
        return self.user.username

#create profile when new user Signs Up
#other methode :@receiver(post_save, sender=User)
def create_profile(sender, instance,created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have the user follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
post_save.connect(create_profile, sender=User)