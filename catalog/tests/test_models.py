import django.core.exceptions
import django.db.transaction
import django.db.utils
from django.test import TestCase

import catalog.models


class ModelTests(TestCase):
    fixtures = ['catalog_fixture.json']

    def test_item_manager(self):
        published_category = catalog.models.Category.objects.get(pk=1)
        published_tag = catalog.models.Tag.objects.get(pk=1)
        unpublished_category = catalog.models.Category.objects.filter(
            is_published=False
        ).get()
        unpublished_tag = catalog.models.Tag.objects.filter(
            is_published=False
        ).get()
        published_item = catalog.models.Item.objects.create(
            is_published=True,
            name='Опубликованный товар',
            category=published_category,
        )
        unpublished_item = catalog.models.Item.objects.create(
            is_published=False,
            name='Неопубликованный товар',
            category=published_category,
        )
        published_item_with_unpublished_category = (
            catalog.models.Item.objects.create(
                is_published=True,
                name='Опубликованный товар с неопубликованной категорией',
                category=unpublished_category,
            )
        )
        published_item.clean()
        published_item.save()
        published_item.tags.add(published_tag, unpublished_tag)
        unpublished_item.clean()
        unpublished_item.save()
        published_item_with_unpublished_category.save()
        published_item_with_unpublished_category.tags.add(published_tag)
        published_item_with_unpublished_category.clean()
        published_items = catalog.models.Item.objects.published()
        self.assertIn(published_tag, published_items[0].tags.all())
        self.assertNotIn(unpublished_tag, published_items[0].tags.all())
        self.assertNotIn(
            published_item_with_unpublished_category, published_items
        )

    def test_tag_manager(self):
        published_tag = catalog.models.Tag.objects.get(pk=1)
        unpublished_tag = catalog.models.Tag.objects.filter(
            is_published=False
        ).get()
        published_tags = catalog.models.Tag.objects.published()
        self.assertIn(published_tag, published_tags)
        self.assertNotIn(unpublished_tag, published_tags)

    def test_item_validator_correct(self):
        item_count = catalog.models.Item.objects.count()
        published_category = catalog.models.Category.objects.get(pk=1)
        published_tag = catalog.models.Tag.objects.get(pk=1)
        self.item = catalog.models.Item(
            name='Test item',
            category=published_category,
            text='Превосходно!Волшебно, замечательно,роскошно!',
        )
        self.item.save()
        self.item.tags.add(published_tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count + 1,
            msg='Doesn`t work with correct data',
        )

    def test_item_validator_negative(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name='Test item',
                text='bitcoinпревосходноbitcoin',
            )
            self.item.full_clean()
            self.item.save()
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
            msg='Works with incorrect data',
        )

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name='Test item',
                text='Аы',
            )
            self.item.full_clean()
            self.item.save()
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
            msg='Works with incorrect data',
        )

    def test_item_creation_without_name(self):
        item_count = catalog.models.Item.objects.count()
        published_category = catalog.models.Category.objects.get(pk=1)
        published_tag = catalog.models.Tag.objects.get(pk=1)
        with self.assertRaises(
            django.core.exceptions.ValidationError,
            msg='Works without a name',
        ):
            self.item = catalog.models.Item(
                category=published_category,
                text='Превосходно',
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(published_tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
            msg='Created without name',
        )

    def test_item_creation_without_category(self):
        item_count = catalog.models.Item.objects.count()
        published_tag = catalog.models.Tag.objects.get(pk=1)
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                text='Превосходно',
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(published_tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
            msg='Created without category',
        )

    def test_item_creation_without_tag(self):
        item_count = catalog.models.Item.objects.count()
        published_category = catalog.models.Category.objects.get(pk=1)
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                category=published_category,
                text='Превосходно',
            )
            self.item.full_clean()
            self.item.save()
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
            msg='Created without tag',
        )

    def test_valid_category_creation(self):
        category_count = catalog.models.Category.objects.count()
        with django.db.transaction.atomic():
            category = catalog.models.Category.objects.create(
                name='New test category',
                slug='url',
            )
            category.save()
            self.assertEqual(
                catalog.models.Category.objects.count(),
                category_count + 1,
                msg='Doesn`t work with correct data',
            )

    def test_category_with_incorrect_slug(self):
        category_count = catalog.models.Category.objects.count()
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with incorrect slug',
            ):
                category = catalog.models.Category.objects.create(
                    name='New test category',
                    slug='FffF-__инвалидслаг$$$__--FF',
                )
                category.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
            msg='Works with invalid slug',
        )

    def test_category_without_name(self):
        category_count = catalog.models.Category.objects.count()
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works without a name,',
            ):
                category = catalog.models.Category.objects.create(slug='url')
                category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
            msg='Works without name',
        )

    def test_category_with_negative_weight(self):
        category_count = catalog.models.Category.objects.count()
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.db.utils.IntegrityError,
                msg='Works with a negative weight',
            ):
                category = catalog.models.Category.objects.create(
                    name='New category',
                    slug='url',
                    weight=-1,
                )
                category.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
            msg='Works with negative weight',
        )

    def test_category_with_too_much_weight(self):
        category_count = catalog.models.Category.objects.count()
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with too big numbers',
            ):
                category = catalog.models.Category.objects.create(
                    name='New category',
                    slug='url',
                    weight=32768,
                )
                category.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
            msg='Works with negative weight',
        )

    def test_category_unique_name(self):
        category_count = catalog.models.Category.objects.count()
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with not unique name',
            ):
                category = catalog.models.Category.objects.create(
                    name='!!люди!!',
                    slug='new-test-tag-slug',
                )
                category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
            msg='Works with not unique name',
        )

    def test_valid_tag(self):
        tag_count = catalog.models.Tag.objects.count()
        with django.db.transaction.atomic():
            tag = catalog.models.Tag.objects.create(
                name='New test tag',
                slug='new-test-tag-slug',
            )
            tag.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count + 1,
            msg='Doesn`t work with valid data',
        )

    def tag_with_invalid_slug(self):
        tag_count = catalog.models.Tag.objects.count()
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with invalid slug',
            ):
                tag = catalog.models.Tag.objects.create(
                    name='New test tag',
                    slug='$.!.()())))((((я хочу спать))))',
                )
                tag.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
            msg='Works with invalid slug',
        )

    def test_tag_with_not_unique_name(self):
        tag_count = catalog.models.Tag.objects.count()
        with self.assertRaises(
            django.core.exceptions.ValidationError,
            msg='Works with not unique name',
        ):
            tag = catalog.models.Tag.objects.create(
                name='(!Кpaсивoe)!',
                slug='beautiful',
            )
            tag.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
            msg='Works with not unique name',
        )

    def test_tag_without_name(self):
        tag_count = catalog.models.Tag.objects.count()
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works without a name',
            ):
                tag = catalog.models.Tag.objects.create(
                    slug='new-test-tag-slug',
                )
                tag.full_clean()
                tag.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
            msg='Works without name',
        )
