import django.db.models

import catalog.models
import catalog.validators


class ValidatedNameField(django.db.models.TextField):
    def __init__(self, protection_table_cls):
        verbose_name = 'Название',
        help_text = 'Добавьте название товара',
        max_length = 150,
        default_validators = [
            catalog.validators.ValidateSameWriting(protection_table_cls)
        ]
        super().__init__(
            verbose_name, help_text, max_length, default_validators,
        )
