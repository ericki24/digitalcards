from django.contrib import admin
from .models import Profile, Experience, SocialLink, ProfileDesign, Subscription


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'profession', 'user')
    search_fields = ('first_name', 'last_name', 'profession', 'user__username', 'primary_email')
    list_filter = ('profession',)
    inlines = [ExperienceInline, SocialLinkInline]


@admin.register(ProfileDesign)
class ProfileDesignAdmin(admin.ModelAdmin):
    list_display = ('profile', 'theme', 'font_family', 'avatar_shape')
    search_fields = ('profile__first_name', 'profile__last_name', 'profile__user__username')
    list_filter = ('theme', 'font_family')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'expires_at', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'user__email')