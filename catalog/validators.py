import django.core.exceptions


class ValidateMustContain:
    def __init__(self, *args, **kwargs):
        self.keywords = args
        self.kwargs = kwargs
        self.message = f'В тексте дожно быть какое-то из слов: {self.keywords}'

    def __call__(self, value):
        for word in self.keywords:
            if word in value.lower():
                return
        raise django.core.exceptions.ValidationError(
            self.message, params={'value': value}
        )

    def __eq__(self, other):
        return self.keywords == other.keywords

    def deconstruct(self):
        path = 'catalog.validators.ValidateMustContain'
        return path, self.keywords, self.kwargs
