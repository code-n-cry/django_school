from django.contrib import admin

from feedback import models


class FilesAdmin(admin.TabularInline):
    model = models.Files
    fields = [models.Files.uploaded_file.field.name]


@admin.register(models.Data)
class FeedbackDataAdmin(admin.ModelAdmin):
    readonly_fields = (models.Data.text.field.name,)
    inlines = (FilesAdmin,)


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = (
        models.Feedback.email.field.name,
        models.Feedback.data.field.name,
    )
