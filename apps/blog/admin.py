from django.contrib import admin

from apps.blog.models import Publication, CommentPublication, PublicationRating, Category


@admin.register(Publication)
class AdminAPublication(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'publication_date',
        'short_description',
        'text',
        'author',
        'category'
    )
    list_filter = ('id', 'publication_date')
    search_fields = ('title', )


@admin.register(CommentPublication)
class AdminCommentPublication(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'publication',
        'created_date',
        'text',
        'active'
    )
    list_filter = ('id', 'created_date')
    search_fields = ('text', )


@admin.register(PublicationRating)
class AdminPublicationRating(admin.ModelAdmin):
    list_display = (
        'rating',
        'user',
        'publication',

    )


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = (
        'name',
    )
