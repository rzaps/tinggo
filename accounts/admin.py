from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_verified', 'is_active', 'created_at')
    list_filter = ('role', 'is_verified', 'is_active', 'language', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'bio', 'avatar')}),
        (_('Location & Preferences'), {'fields': ('country', 'city', 'language')}),
        (_('Role & Status'), {'fields': ('role', 'is_verified', 'is_active')}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'language', 'password1', 'password2'),
        }),
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = _('Full Name')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'website', 'created_at')
    list_filter = ('email_notifications', 'push_notifications', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'business_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Social Media'), {'fields': ('website', 'instagram', 'facebook', 'twitter')}),
        (_('Business Information'), {'fields': ('business_name', 'business_description')}),
        (_('Preferences'), {'fields': ('email_notifications', 'push_notifications')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    readonly_fields = ('created_at', 'updated_at')
