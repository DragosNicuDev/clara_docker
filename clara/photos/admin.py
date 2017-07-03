from django.contrib import admin
from .models import PhotoUpload
from django.utils.html import mark_safe
from django.utils import timezone
from django.contrib.admin.actions import delete_selected


# The Admin view for the Photo App
class PhotoUploadAdmin(admin.ModelAdmin):
    fields = (
        'image_tag',
        'image',
        'status',
        'date_upload',
        'date_approved',
        'date_deleted',
        'user',
        'pause_upload')
    list_display = (
        'image_tag',
        'pause_upload',
        'user',
        'status',
        'date_upload',
        'date_approved',
        'date_deleted')
    readonly_fields = (
        'image_tag',
        'date_upload',
        'date_approved',
        'date_deleted')
    list_filter = ('status', 'user')
    actions = ['make_published', 'soft_delete']
    # Rename delete selected
    delete_selected.short_description = "Permanently delete selected"

    # Admin action
    def make_published(self, request, queryset):
        # Updates the status to approved
        queryset.update(status='ap')
        # and the date when modified
        date = timezone.now()
        queryset.update(date_approved=date)
    make_published.short_description = "Mark selected photos as Approved"

    def soft_delete(self, request, queryset):
        # Updates the status to deleted
        queryset.update(status='tr')
        # and the date when modified
        date_delete = timezone.now()
        queryset.update(date_deleted=date_delete)
    soft_delete.short_description = "Move to Trash"

    # Admin thumbnail view
    def image_tag(self, obj):
        return mark_safe('<img src="%s" width="150"/>' % (obj.image.url))
    image_tag.short_description = 'On site photo'


admin.site.register(PhotoUpload, PhotoUploadAdmin)
