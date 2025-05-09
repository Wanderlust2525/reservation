from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id', 'username', 'get_full_name', 'role', 'get_avatar'
    )
    list_display_links = ('id', 'username')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Личная информация'), {'fields': (
            'avatar', 'get_avatar', 'first_name', 'last_name'
        )}),
        (_('Роли и доступ'), {'fields': (
            'role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
        )}),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','password1', 'password2', 'role'),
        }),
    )

    readonly_fields = ('get_avatar', 'date_joined', 'last_login')

    @admin.display(description=_('Аватарка'))
    def get_avatar(self, user):
        if user.avatar:
            return mark_safe(f'<img src="{user.avatar.url}" alt="{user.username}" width="100px" />')
        return '-'


# Register your models here.
