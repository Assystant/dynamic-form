import json
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework import serializers
from .models import (Field, FieldOption, FieldValidation, Section, Template,
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
                f"Cannot attach options to {value.type} field."
            )
        return value


class FieldSerializer(ModelSerializer):
    validations = FieldValidationSerializer(
        many=True,
        required=False,
        read_only=True)
    template = PrimaryKeyRelatedField(read_only=True)
    options = FieldOptionSerializer(many=True, required=False)
    file_types = serializers.ListField(
        child=serializers.CharField(max_length=100),
        allow_empty=True,
        required=False)

    class Meta:
        model = Field
        exclude = ['created', 'modified',]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['file_types'] = instance.file_types_list
        return representation

    def create(self, validated_data):
        raw_options_data = validated_data.pop('options', [])
        file_types_data = json.dumps(validated_data.pop('file_types', ''))
        field = Field.objects.create(**validated_data)
        field.file_types = file_types_data
        field.save()
        for raw_data in raw_options_data:
            field_serializer = FieldOptionSerializer(data=raw_data)
            field_serializer.is_valid(raise_exception=True)
            field_serializer.save(field=field)
        return field

    def update(self, instance, validated_data):
        # raw_options_data = self.data.get('options', [])
        options_data = validated_data.pop('options', [])
        instance.label = validated_data.get('label', instance.label)
        instance.placeholder = validated_data.get(
            'placeholder', instance.placeholder)
        instance.required = validated_data.get(
            'required', instance.required)
        instance.sort_score = validated_data.get(
            'sort_score', instance.sort_score)
        instance.allow_specific_file_type = validated_data.get(
            'allow_specific_file_type', instance.allow_specific_file_type)
        instance.file_types_list = validated_data.get(
            'file_types', instance.file_types_list)
        instance.save()
        for option_data in options_data:
            print(option_data)
            option_instance = None
            try:
                option_instance = instance.options.get(pk=option_data.get('id', None))
            except:
                pass
            serializer = FieldOptionSerializer(option_instance, data=option_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(field=instance)
        return instance


class SectionSerializer(ModelSerializer):
    fields = FieldSerializer(many=True, required=False)

    class Meta:
        model = Section
        exclude = ['created', 'modified']


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
    sections = SectionSerializer(many=True, required=False)

    class Meta:
        model = Template
        exclude = ['created', 'modified',]

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        template = Template.objects.create(**validated_data)
        for raw_data in fields_data:
            field_serializer = FieldSerializer(data=raw_data)
            field_serializer.is_valid(raise_exception=True)
            field_serializer.save(template=template)
        return template

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', [])
        instance.label = validated_data.get('label', instance.label)
        instance.description = validated_data.get(
            'description',
            instance.description)
        instance.save()
        for field_data in fields_data:
            print(field_data)
            field_instance = None
            try:
                field_instance = instance.fields.get(
                    pk=field_data.get('id', None))
            except Template.DoesNotExist:
                pass
            serializer = FieldSerializer(field_instance, data=field_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(template=instance)
        return instance
