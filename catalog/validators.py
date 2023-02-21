import re

import django.core.exceptions


class ValidateMustContain:
    def __init__(self, *args, **kwargs):
        self.keywords = [i.lower() for i in args]
        self.kwargs = kwargs
        self.message = 'В тексте дожно быть какое-то из слов: %(value)s'

    def __call__(self, value):
        splitted_value = re.split(r'[,!?.(): -]', value.lower())
        for word in splitted_value:
            if word in self.keywords:
                return
        raise django.core.exceptions.ValidationError(
            self.message, params={'value': ', '.join(self.keywords)}
        )

    def __eq__(self, other):
        return self.keywords == other.keywords

    def deconstruct(self):
        path = 'catalog.validators.ValidateMustContain'
        return path, self.keywords, self.kwargs
