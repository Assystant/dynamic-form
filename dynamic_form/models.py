import json

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class Template(TimeStampedModel):
    label = models.CharField(max_length=5000, default='', blank=True)
    description = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"template_id : {self.id} --> {self.label}"


class Section(TimeStampedModel):
    label = models.CharField(max_length=5000, default='', blank=True)
    description = models.TextField(blank=True, default="")
    template = models.ForeignKey(
        Template,
        related_name="sections",
        blank=True,
        on_delete=models.CASCADE)
    sort_order = models.PositiveBigIntegerField(default=0, blank=True)
    # fields = models.ManyToManyField(Field, blank=True)


class Field(TimeStampedModel):
    TEXT = 'TEXT'
    TEXTAREA = 'TEXTAREA'
    RADIO = 'RADIO'
    CHECKBOX = 'CHECKBOX'
    DROPDOWN = 'DROPDOWN'
    MULTISELECT = 'MULTISELECT'
    FILEUPLOAD = 'FILEUPLOAD'
    CURRENCY = 'CURRENCY'
    PHONE = 'PHONE'
    NAME = 'NAME'
    EMAIL = 'EMAIL'
    DATE = 'DATE'

    FIELD_TYPE = [
        (TEXT, 'Text'),
        (TEXTAREA, 'Textarea'),
        (RADIO, 'Radio'),
        (CHECKBOX, 'Checkbox'),
        (DROPDOWN, 'Dropdown'),
        (MULTISELECT, 'MultiSelect'),
        (FILEUPLOAD, 'FileUpload'),
        (CURRENCY, 'Currency'),
        (PHONE, 'Phone'),
        (NAME, 'Name'),
        (EMAIL, 'Email'),
        (DATE, 'Date'),
    ]
    type = models.CharField(
        max_length=100,
        choices=FIELD_TYPE,
        default=TEXT,
        blank=True)
    label = models.CharField(max_length=5000, default='', blank=True)
    placeholder = models.CharField(max_length=5000, default='', blank=True)
    required = models.BooleanField(default=True, blank=True)
    # uuid = models.UUIDField(unique=True)
    template = models.ForeignKey(
        Template,
        related_name="fields",
        blank=True,
        on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section,
        related_name='fields',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    sort_score = models.IntegerField(default=0, blank=True)
    allow_specific_file_type = models.BooleanField(default=False, blank=True)
    file_types = models.TextField(blank=True, default="[]")
    maximum_files = models.PositiveIntegerField(default=1, blank=True)
    maximum_size = models.PositiveIntegerField(
        default=1, help_text="In MB", blank=True)

    @property
    def file_types_list(self):
        return json.loads(self.file_types)

    @file_types_list.setter
    def file_types_list(self, value):
        self.file_types = json.dumps(value)

    def __str__(self) -> str:
        return f"template_id : {self.template_id} --> field_id : {self.id} --> {self.type}"


class FieldValidation(TimeStampedModel):
    logic = models.TextField(max_length=5000, default='', blank=True)
    field = models.ForeignKey(
        Field,
        related_name="validations",
        blank=True,
        on_delete=models.CASCADE)


class FieldOption(TimeStampedModel):
    label = models.CharField(max_length=5000, default='', blank=True)
    sort_score = models.IntegerField(default=0, blank=True)
    field = models.ForeignKey(
        Field,
        related_name="options",
        blank=True,
        on_delete=models.CASCADE)


class UserInputTextValue(TimeStampedModel):
    text = models.TextField(max_length=5000, blank=True, default='')


class UserInputAttachment(TimeStampedModel):
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')


class UserInput(TimeStampedModel):
    user = models.ForeignKey(
        User,
        related_name="input_values",
        blank=True,
        on_delete=models.CASCADE)
    field = models.ForeignKey(
        Field,
        related_name="input_values",
        blank=True,
        on_delete=models.CASCADE)
    template = models.ForeignKey(
        Template,
        related_name="input_values",
        blank=True,
        on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    value = GenericForeignKey()
