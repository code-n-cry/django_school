import django.core.exceptions
import django.db.transaction
import django.db.utils
from django.test import TestCase

import catalog.models


class ModelTests(TestCase):
    def setUp(self):
        self.category = catalog.models.Category.objects.create(
            is_published=True,
            name='Test category',
            slug='test-category-slug',
        )
        self.category.save()
        self.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name='Test tag',
            slug='test-tag-slug',
        )
        self.tag.save()
        super().setUp()

    def tearDown(self):
        catalog.models.Item.objects.all().delete()
        catalog.models.Category.objects.all().delete()
        catalog.models.Tag.objects.all().delete()
        super().tearDown()

    def test_item_manager(self):
        unpublished_category = catalog.models.Category.objects.create(
            is_published=False,
            name='Неопубликованная тестовая категория',
            slug='unpublished_category',
        )
        unpublished_tag = catalog.models.Tag.objects.create(
            is_published=False,
            name='Неопубликованный тестовый тег',
            slug='unpublished_tag',
        )
        unpublished_category.save()
        unpublished_tag.save()
        published_item = catalog.models.Item.objects.create(
            is_published=True,
            is_on_main=True,
            name='Опубликованный товар',
            category=self.category,
        )
        unpublished_item = catalog.models.Item.objects.create(
            is_published=False,
            is_on_main=True,
            name='Неопубликованный товар',
            category=self.category,
        )
        published_item_with_unpublished_category = (
            catalog.models.Item.objects.create(
                is_published=True,
                is_on_main=True,
                name='Опубликованный товар с неопубликованной категорией',
                category=unpublished_category,
            )
        )
        published_item.clean()
        published_item.save()
        published_item.tags.add(self.tag, unpublished_tag)
        unpublished_item.clean()
        unpublished_item.save()
        published_item_with_unpublished_category.save()
        published_item_with_unpublished_category.tags.add(self.tag)
        published_item_with_unpublished_category.clean()
        published_items = catalog.models.Item.objects.published()
        self.assertIn(self.tag, published_items[0].tags.all())
        self.assertNotIn(unpublished_tag, published_items[0].tags.all())
        self.assertNotIn(
            published_item_with_unpublished_category, published_items
        )

    def test_tag_manager(self):
        unpublished_tag = catalog.models.Tag.objects.create(
            is_published=False,
            name='Неопубликованный тестовый тег',
            slug='unpublished_tag',
        )
        published_tags = catalog.models.Tag.objects.published()
        self.assertIn(self.tag, published_tags)
        self.assertNotIn(unpublished_tag, published_tags)

    def test_item_validator_correct(self):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name='Test item',
            category=self.category,
            text='Превосходно!Волшебно, замечательно,роскошно!',
        )
        self.item.save()
        self.item.tags.add(self.tag)
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
                category=self.category,
                text='bitcoinпревосходноbitcoin',
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
            msg='Works with incorrect data',
        )

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name='Test item',
                category=self.category,
                text='Аы',
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
            msg='Works with incorrect data',
        )

    def test_item_creation_without_name(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(
            django.core.exceptions.ValidationError,
            msg='Works without a name',
        ):
            self.item = catalog.models.Item(
                category=self.category,
                text='Превосходно',
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
            msg='Created without name',
        )

    def test_item_creation_without_category(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                text='Превосходно',
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
            msg='Created without category',
        )

    def test_item_creation_without_tag(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                category=self.category,
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
            self.category = catalog.models.Category.objects.create(
                name='New test category',
                slug='url',
            )
            self.category.save()
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
                self.category = catalog.models.Category.objects.create(
                    name='New test category',
                    slug='FffF-__инвалидслаг$$$__--FF',
                )
                self.category.full_clean()
                self.category.save()
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
                self.category = catalog.models.Category.objects.create(
                    slug='url'
                )
                self.category.full_clean()
                self.category.save()

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
                self.category = catalog.models.Category.objects.create(
                    name='New category',
                    slug='url',
                    weight=-1,
                )
                self.category.full_clean()
                self.category.save()
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
                self.category = catalog.models.Category.objects.create(
                    name='New category',
                    slug='url',
                    weight=32768,
                )
                self.category.full_clean()
                self.category.save()
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
                self.category = catalog.models.Category.objects.create(
                    name='!!Test,category!!',
                    slug='new-test-tag-slug',
                )
                self.category.full_clean()
                self.category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
            msg='Works with not unique name',
        )

    def test_valid_tag(self):
        tag_count = catalog.models.Tag.objects.count()
        with django.db.transaction.atomic():
            self.tag = catalog.models.Tag.objects.create(
                name='New test tag',
                slug='new-test-tag-slug',
            )
            self.tag.save()

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
                self.tag = catalog.models.Tag.objects.create(
                    name='New test tag',
                    slug='$.!.()())))((((я хочу спать))))',
                )
                self.tag.full_clean()
                self.tag.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
            msg='Works with invalid slug',
        )

    def test_tag_with_not_unique_name(self):
        tag_count = catalog.models.Tag.objects.count()
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with not unique name',
            ):
                self.tag = catalog.models.Tag.objects.create(
                    name='Test tag',
                    slug='slg',
                )
                self.tag.full_clean()
                self.tag.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
            msg='Works with not unique name',
        )

        self.tearDown()

        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with not unique name',
            ):
                self.tag = catalog.models.Tag.objects.create(
                    name='(!1Test,tag1!)',
                    slug='slg',
                )
                self.tag.full_clean()
                self.tag.save()

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
                self.tag = catalog.models.Tag.objects.create(
                    slug='new-test-tag-slug',
                )
                self.tag.full_clean()
                self.tag.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
            msg='Works without name',
        )
