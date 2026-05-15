from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from .models import Image


def image_caption(obj):
    return obj.caption


image_caption.short_description = 'Caption'


def from_menu(obj):
    return bool(obj.menu_item)


from_menu.boolean = True
from_menu.short_description = 'From Menu'


@admin.register(Image)
class ImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', image_caption, 'uploaded_at', from_menu)
    search_fields = ('title',)
    autocomplete_fields = ('menu_item',)
