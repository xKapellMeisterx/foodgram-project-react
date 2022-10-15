from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'hexcolor', 'slug')


