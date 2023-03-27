from django.contrib import admin

import catalog.models


class MainImageAdmin(admin.TabularInline):
    model = catalog.models.ItemMainImage
    readonly_fields = (catalog.models.ItemMainImage.image_tmb,)


class ImageGalleryAdmin(admin.TabularInline):
    model = catalog.models.ItemDescriptionsImages
    fields = [catalog.models.ItemDescriptionsImages.image.field.name]


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        'get_image',
    )
    inlines = [MainImageAdmin, ImageGalleryAdmin]
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)

    @admin.display(ordering='main_image', description='Фото товара')
    def get_image(self, obj):
        return obj.main_image.image_tmb()


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Category.name.field.name,
        catalog.models.Category.is_published.field.name,
    )
    list_editable = (catalog.models.Category.is_published.field.name,)


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Tag.name.field.name,
        catalog.models.Tag.is_published.field.name,
    )
    list_editable = (catalog.models.Tag.is_published.field.name,)
