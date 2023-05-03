from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import Profile
# Register your models here.
#unregister groups
admin.site.unregister(Group)

#Mix both of profile and user into one 
class ProfileInline(admin.StackedInline):
        model = Profile

#extend user model
class UserAdmin(admin.ModelAdmin):
        model =User

        #just display username fields on admin page
        fields=["username"]
        inlines = [ProfileInline]

#unregister initial User
admin.site.unregister(User)
#reregister User and Profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)


