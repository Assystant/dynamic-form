from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import (Field, FieldOption, FieldValidation, Template,
                     UserInput, UserInputAttachment, UserInputTextValue)


class FieldValidationSerializer(ModelSerializer):
    class Meta:
        model = FieldValidation
        exclude = ['created', 'modified',]


class FieldOptionSerializer(ModelSerializer):
    class Meta:
        model = FieldOption
        exclude = ['created', 'modified',]

    def validate_field(self, value):
        if value.type not in [Field.RADIO, Field.CHECKBOX, Field.DROPDOWN]:
            raise serializers.ValidationError(
                f"cannot attach options to {value.type} field."
            )
        return value


class FieldSerializer(ModelSerializer):
    validations = FieldValidationSerializer(many=True, required=False)
    options = FieldOptionSerializer(many=True, required=False)

    class Meta:
        model = Field
        exclude = ['created', 'modified',]


class InputTextSerializer(ModelSerializer):
    class Meta:
        model = UserInputTextValue
        exclude = ['created', 'modified',]


class InputAttachmentSerializer(ModelSerializer):
    class Meta:
        model = UserInputAttachment
        exclude = ['created', 'modified',]


class UserInputSerializer(ModelSerializer):
    class Meta:
        model = UserInput
        exclude = ['created', 'modified',]


class TemplateSerializer(ModelSerializer):
    fields = FieldSerializer(many=True, required=False)

    class Meta:
        model = Template
        exclude = ['created', 'modified',]
