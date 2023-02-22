import re

import django.core.exceptions


class ValidateMustContain:
    def __init__(self, *args, **kwargs):
        self.keywords = [i.lower() for i in args]
        self.kwargs = kwargs
        self.message = 'В тексте дожно быть какое-то из слов: %(value)s'

    def __call__(self, value):
        text = re.findall(r'\b.*?\b', value.lower())
        is_wrong = True
        for word in text:
            if word in self.keywords:
                is_wrong = False
                break
        if is_wrong:
            raise django.core.exceptions.ValidationError(self.message)
        return value

    def __eq__(self, other):
        return self.keywords == other.keywords

    def deconstruct(self):
        path = 'catalog.validators.ValidateMustContain'
        return path, self.keywords, self.kwargs
