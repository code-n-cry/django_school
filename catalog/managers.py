import django.db.models

import catalog.models


class ItemManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related(
                catalog.models.Item.main_image.related.related_name
            )
            .select_related(catalog.models.Item.category.field.name)
            .prefetch_related(
                django.db.models.Prefetch(
                    catalog.models.Item.tags.field.name,
                    queryset=catalog.models.Tag.objects.published(),
                )
            )
            .only(
                catalog.models.Item.id.field.name,
                catalog.models.Item.name.field.name,
                catalog.models.Item.text.field.name,
                '__'.join(
                    [
                        catalog.models.Item.category.field.name,
                        catalog.models.Category.name.field.name,
                    ]
                ),
                '__'.join(
                    [
                        catalog.models.Item.main_image.related.related_name,
                        catalog.models.ItemMainImage.image.field.name,
                    ]
                ),
            )
            .order_by(catalog.models.Item.name.field.name)
        )


class TagManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .only(catalog.models.Tag.name.field.name)
        )
