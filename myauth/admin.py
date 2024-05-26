from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from myauth.models import User, UserLocation

class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm
    list_display = ('email', 'username')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_banned')}),
        ('Personal info', {'fields': ('avatar_url', 'username', 'phone_number', 'location', 'user_type', 'about', 'achievements')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count')
    readonly_fields = ('user_count',)

    def user_count(self, obj):
        return obj.user_count

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserLocation, UserLocationAdmin)
