from django.contrib import admin

from feedback import models


class FilesAdmin(admin.TabularInline):
    model = models.Files
    fields = [models.Files.uploaded_file.field.name]


class FeedbackDataAdmin(admin.TabularInline):
    model = models.PersonalData
    fields = [models.PersonalData.email.field.name]


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = (models.Feedback.text.field.name,)
    inlines = (
        FilesAdmin,
        FeedbackDataAdmin,
    )
