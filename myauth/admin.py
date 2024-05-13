from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from myauth.models import User

class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm
    list_display = ('email', 'username')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('avatar_url', 'username', 'phone_number', 'location', 'user_type', 'about', 'achievements')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(User, CustomUserAdmin)
