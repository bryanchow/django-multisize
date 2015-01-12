from django.contrib import admin
from .models import ResizedImage


class ResizedImageAdmin(admin.ModelAdmin):

    list_display = [
        'source_type',
        'source_id',
        'width',
        'height',
        'quality',
        'should_crop',
        'created',
        'modified',
    ]
    readonly_fields = [
        'created',
        'modified',
    ]

admin.site.register(ResizedImage, ResizedImageAdmin)
