from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin

from .models import Category, Item, SubItem


class SubItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SubItem
    extra = 1


@admin.register(Item)
class ItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'name', 'price', 'active', 'category')
    list_filter = ('active', 'category')
    search_fields = ('name', 'description')
    inlines = [SubItemInline]


@admin.register(SubItem)
class SubItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'details', 'price', 'item')
    search_fields = ('details',)


class ItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Item
    extra = 1


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'name', 'description')
    search_fields = ('name', 'description')
    inlines = [ItemInline]
