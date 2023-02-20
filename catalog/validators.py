import difflib

import django.core.exceptions


class ValidateMustContain:
    def __init__(self, *args, **kwargs):
        self.keywords = args
        self.kwargs = kwargs
        self.message = 'В тексте дожно быть какое-то из слов: %(value)s'

    def __call__(self, value):
        for word in self.keywords:
            if word in value.lower():
                return
        raise django.core.exceptions.ValidationError(
            self.message, params={'value': self.keywords}
        )

    def __eq__(self, other):
        return self.keywords == other.keywords

    def deconstruct(self):
        path = 'catalog.validators.ValidateMustContain'
        return path, self.keywords, self.kwargs


class ValidateSameWriting:
    def __init__(self, protection_table_cls, *args, **kwargs):
        self.cls = protection_table_cls
        self.args = args
        self.kwargs = kwargs
        self.message = 'Текущее название слишком похоже на уже существующее!'
        self.path = 'catalog.validators.ValidateSameWriting'

    def __call__(self, value):
        unique_names = self.cls.objects.all()
        for obj in unique_names:
            if obj.name == value:
                return
            if (
                difflib.SequenceMatcher(
                    a=obj.name.lower(), b=value.lower()
                ).ratio()
                > 0.6
            ):
                raise django.core.exceptions.ValidationError(self.message)
        else:
            new_name = self.cls.objects.create(name=value)
            new_name.save()
            return

    def __eq__(self, other):
        return self.cls == other.cls

    def deconstruct(self):
        return self.path, self.args, self.kwargs
