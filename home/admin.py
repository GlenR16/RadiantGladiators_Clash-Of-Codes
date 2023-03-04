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
        ('User Data', {'fields': ('email', 'name', 'phone','is_verified','verification_file')}),
        ('NGO Data', {'fields': ('latitude', 'longitude', 'active_members','tickets','address','website','about')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions','password')}),  
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('id',)

admin.site.register(Interest)
admin.site.register(Swipe)
