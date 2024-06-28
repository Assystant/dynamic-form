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
    validations = FieldValidationSerializer(
        many=True,
        required=False,
        read_only=True)
    options = FieldOptionSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Field
        exclude = ['created', 'modified',]

    def create(self, validated_data):
        raw_options_data = self.data.get('options', [])
        field = Field.objects.create(**validated_data)
        for raw_data in raw_options_data:
            field_serializer = FieldOptionSerializer(data=raw_data)
            field_serializer.is_valid(True)
            field_serializer.save(field=field)
        return field

    def update(self, instance, validated_data):
        pass


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
    fields = FieldSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Template
        exclude = ['created', 'modified',]

    def create(self, validated_data):
        raw_fields_data = self.data.get('fields', [])
        template = Template.objects.create(**validated_data)
        for raw_data in raw_fields_data:
            field_serializer = FieldSerializer(data=raw_data)
            field_serializer.is_valid(True)
            field_serializer.save(template=template)
        return template

    def update(self, instance, validated_data):
        pass
