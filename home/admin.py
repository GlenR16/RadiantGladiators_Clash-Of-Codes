from django.contrib.admin.decorators import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Interest,Swipe
from .forms import UserChangeForm,UserCreationForm
# Register your models here.

@register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'name',)
    list_filter = ('id_is_verified', 'is_active')
    fieldsets = (
        ('User Data', {'fields': ('email', 'name', 'phone','country',"id_is_verified",'verification_file','status','dob','gender','who_to_date')}),
        ('Data', {'fields': ('bio','profile_image','likes','dislikes','face_detection_probablity','address','college','otp','insta_username','user_score','height','interests','is_habit_drink','is_habit_smoke','premium')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions','password')}),  
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1','dob', 'phone', 'verification_file', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('id',)

admin.site.register(Interest)
admin.site.register(Swipe)
