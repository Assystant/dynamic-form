from .models import *
from django.contrib import admin

# admin.site.register(Template)
# admin.site.register(Field)
admin.site.register(FieldValidation)
admin.site.register(FieldOption)
admin.site.register(UserInputTextValue)
admin.site.register(UserInputAttachment)
admin.site.register(UserInput)


class FieldInline(admin.TabularInline):
    model = Field
    extra = 1

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    inlines = [FieldInline]
    
    
class FieldOptionInline(admin.TabularInline):
    model = FieldOption
    extra = 1

class FieldValidationInline(admin.TabularInline):
    model = FieldValidation
    extra = 1

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    inlines = [FieldOptionInline, FieldValidationInline]
    search_fields = ('template__id',)
    list_filter = ('type', 'required')

