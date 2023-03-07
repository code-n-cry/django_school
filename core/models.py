import re
import string

import django.core.exceptions
import django.core.validators
import django.db.models
import django.utils.html
import sorl.thumbnail


class PublishedWithNameBaseModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        verbose_name='опубликовать?',
        help_text='Выберите статус публикации',
        default=True,
    )
    name = django.db.models.CharField(
        verbose_name='название',
        help_text='Добавьте название',
        max_length=150,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]


class SlugBaseModel(PublishedWithNameBaseModel):
    slug = django.db.models.SlugField(
        'слаг',
        help_text='Напишите код для url(латинские буквы, цифры и `-`, `_`)',
        max_length=200,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class UniqueNameSlugBaseModel(SlugBaseModel):
    is_cleaned = False
    similar_english_to_russian_letters = {
        'a': 'а',
        'e': 'е',
        'p': 'р',
        'o': 'о',
        'x': 'х',
        'y': 'у',
        'c': 'с',
        't': 'т',
        'h': 'н',
        'b': 'в',
        'k': 'к',
        'm': 'м',
    }
    msg = 'Кажется, похожее название уже существует!'
    unique_name = django.db.models.CharField(
        verbose_name='уникальное имя',
        help_text='Колонка для проверки уникальности названия',
        max_length=150,
        unique=True,
        null=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def generate_normalized_name(self):
        normalized_name_english = ''
        normalized_name_russian = ''
        for letter in list(
            ''.join(re.split(f'[{string.punctuation} ]', self.name.lower()))
        ):
            if letter:
                for (
                    eng_letter,
                    rus_letter,
                ) in self.similar_english_to_russian_letters.items():
                    if letter == eng_letter:
                        normalized_name_english += letter
                        normalized_name_russian += rus_letter
                        break
                    if letter == rus_letter:
                        normalized_name_russian += letter
                        normalized_name_english += eng_letter
                        break
                else:
                    normalized_name_russian += letter
                    normalized_name_english += letter
        name_checking_1 = self.__class__.objects.filter(
            unique_name=normalized_name_english
        )
        name_checking_2 = self.__class__.objects.filter(
            unique_name=normalized_name_russian
        )
        if not name_checking_1 and not name_checking_2:
            self.unique_name = normalized_name_russian
            return super().clean()
        raise django.core.exceptions.ValidationError(self.msg)

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        self.is_cleaned = True
        self.generate_normalized_name()


class ImageModel(django.db.models.Model):
    image = django.db.models.ImageField(
        'изображение(будет масштабировано до 300x300)',
        help_text='загрузите картинки для уточнения описания',
        upload_to='uploaded/',
    )

    class Meta:
        abstract = True

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image, '300x300', crop='center', quality=65
        )

    def image_tmb(self):
        if self.image:
            return django.utils.html.mark_safe(
                f'<img src="{self.get_image_300x300().url}">'
            )
        self.image_tmb.short_description = 'превью'
        return '(Фото товара)'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.image = self.get_image_300x300()
