from django.contrib import admin

from apps.users.models import AuthorProfile


@admin.register(AuthorProfile)
class AdminAuthorProfile(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'avatar',
        'email',
        'phone',
        'skype'
    )
    list_filter = ('id',)
    search_fields = ('last_name', 'email')
