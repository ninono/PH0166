from django.contrib import admin
from pslechdb.models import *
from nested_inline.admin import NestedModelAdmin,NestedStackedInline
from django import forms
from redactor.widgets import RedactorEditor
# Register your models here.

class SolutionInline(NestedStackedInline):
    model=Solution
    extra=0

class QuestionInline(NestedStackedInline):
    model=Question
    inlines=[SolutionInline,]
    formfield_overrides = {
        models.TextField: {'widget': RedactorEditor(),},
    }
    extra=0

@admin.register(Passage)
class PassageAdmin(NestedModelAdmin):
    inlines=[QuestionInline,]
    formfield_overrides = {
        models.TextField: {'widget': RedactorEditor(),},
    }

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass

@admin.register(QTag)
class QTagAdmin(admin.ModelAdmin):
    pass
@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    pass
@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    formfield_overrides={
        models.TextField: {'widget': RedactorEditor(),},
    }
