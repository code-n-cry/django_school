import django.core.exceptions
import django.db.transaction
import django.db.utils
from django.test import TestCase

import catalog.models


class ModelTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name='Test category',
            slug='test-category-slug',
        )
        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name='Test tag',
            slug='test-tag-slug',
        )
        cls.item_count = catalog.models.Item.objects.count()
        cls.category_count = catalog.models.Category.objects.count()
        cls.tags_count = catalog.models.Tag.objects.count()
        return super().setUpClass()

    def tearDown(self):
        self.category = catalog.models.Category.objects.all().delete()
        self.item = catalog.models.Item.objects.all().delete()
        self.tag = catalog.models.Tag.objects.all().delete()
        self.item_count = catalog.models.Item.objects.count()
        self.category_count = catalog.models.Category.objects.count()
        self.tags_count = catalog.models.Tag.objects.count()
        return super().tearDown()

    def test_item_validator_correct(self):
        self.item = catalog.models.Item(
            name='Test item',
            category=self.category,
            text='Превосходно!Волшебно, замечательно,роскошно!',
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            self.item_count + 1,
            msg='Doesn`t work with correct data',
        )

    def test_item_validator_negative(self):
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
            self.item_count,
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
            self.item_count,
            msg='Works with incorrect data',
        )

    def test_invalid_item_creation(self):
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
            self.item_count,
            msg='Created without name',
        )

        with self.subTest('No category'):
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.item = catalog.models.Item(
                    text='Превосходно',
                )
                self.item.full_clean()
                self.item.save()
                self.item.tags.add(self.tag)

            self.assertEqual(
                catalog.models.Item.objects.count(),
                self.item_count,
                msg='Created without category',
            )

        with self.subTest('No tags'):
            with self.assertRaises(django.core.exceptions.ValidationError):
                self.item = catalog.models.Item(
                    category=self.category,
                    text='Превосходно',
                )
                self.item.full_clean()
                self.item.save()

            self.assertEqual(
                catalog.models.Item.objects.count(),
                self.item_count,
                msg='Created without tag',
            )

    def test_valid_category(self):
        with django.db.transaction.atomic():
            self.category = catalog.models.Category.objects.create(
                name='Testy category 1',
                slug='url',
            )
            self.category.full_clean()
            self.category.save()
            self.assertEqual(
                catalog.models.Category.objects.count(),
                self.category_count + 1,
                msg='Doesn`t work with correct data',
            )

    def test_invalid_category(self):
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with incorrect slug',
            ):
                self.category = catalog.models.Category.objects.create(
                    name='New category 2',
                    slug='FffF-__инвалидслаг$$$__--FF',
                )
                self.category.full_clean()
                self.category.save()
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works without a name,',
            ):
                self.category = catalog.models.Category.objects.create(
                    slug='new-test-slug-3'
                )
                self.category.full_clean()
                self.category.save()

        with django.db.transaction.atomic():
            with self.assertRaises(
                django.db.utils.IntegrityError,
                msg='Works with a negative weight',
            ):
                self.category = catalog.models.Category.objects.create(
                    name='Category for test',
                    slug='test-slug-4',
                    weight=-1,
                )
                self.category.full_clean()
                self.category.save()

        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with too big numbers',
            ):
                self.category = catalog.models.Category.objects.create(
                    name='butterfly',
                    slug='test-slug-4',
                    weight=32768,
                )
                self.category.full_clean()
                self.category.save()

        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with not unique name',
            ):
                self.category = catalog.models.Category.objects.create(
                    name='Test category',
                    slug='slg',
                )
                self.category.full_clean()
                self.category.save()

    def test_category_unique_name(self):
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with not unique name',
            ):
                self.category = catalog.models.Category.objects.create(
                    name='!!Test,category!!',
                    slug='slg',
                )
                self.category.full_clean()
                self.category.save()

        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with not unique name',
            ):
                self.category = catalog.models.Category.objects.create(
                    name='(!1Test,category1!)',
                    slug='slg',
                )
                self.category.full_clean()
                self.category.save()

    def test_valid_tag(self):
        with django.db.transaction.atomic():
            self.tag = catalog.models.Tag.objects.create(
                name='New tag',
                slug='new-test-tag-slug',
            )
            self.tag.full_clean()
            self.tag.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                self.tags_count + 1,
                msg='Doesn`t work with valid data',
            )

    def test_invalid_tag(self):
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with invalid slug',
            ):
                self.tag = catalog.models.Tag.objects.create(
                    name='Test tag 2',
                    slug='$.!.()())))((((я хочу спать))))',
                )
                self.tag.full_clean()
                self.tag.save()

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

    def test_tag_unique_name(self):
        with django.db.transaction.atomic():
            with self.assertRaises(
                django.core.exceptions.ValidationError,
                msg='Works with not unique name',
            ):
                self.tag = catalog.models.Tag.objects.create(
                    name='!!Test,tag!!',
                    slug='slg',
                )
                self.tag.full_clean()
                self.tag.save()

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
