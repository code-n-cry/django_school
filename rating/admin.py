from django.contrib import admin

from rating import models


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        models.Rating.item.field.name,
        models.Rating.user.field.name,
        models.Rating.rating.field.name,
    )
