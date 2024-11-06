from .models import (Field, FieldOption, FieldValidation, Template,
                     UserInput, UserInputAttachment, UserInputTextValue)
from .serializers import (FieldOptionSerializer, FieldSerializer,
                          FieldValidationSerializer, InputAttachmentSerializer,
                          InputTextSerializer, TemplateSerializer,
                          UserInputSerializer)
from rest_framework.viewsets import ModelViewSet


class TemplateViewSet(ModelViewSet):
    serializer_class = TemplateSerializer
    queryset = Template.objects.all()


class FieldViewSet(ModelViewSet):
    serializer_class = FieldSerializer
    # queryset = Field.objects.all()

    def get_queryset(self):
        queryset = Field.objects.all()
        template_id = self.request.query_params.get('template')
        if template_id:
            queryset = queryset.filter(template_id=template_id)
        return queryset


class FieldValidationViewSet(ModelViewSet):
    serializer_class = FieldValidationSerializer
    # queryset = FieldValidation.objects.all()

    def get_queryset(self):
        queryset = FieldValidation.objects.all()
        field_id = self.request.query_params.get('field')
        if field_id:
            queryset = queryset.filter(template_id=field_id)
        return queryset


class FieldOptionViewSet(ModelViewSet):
    serializer_class = FieldOptionSerializer
    queryset = FieldOption.objects.all()

    def get_queryset(self):
        queryset = FieldOption.objects.all()
        field_id = self.request.query_params.get('field')
        if field_id:
            queryset = queryset.filter(template_id=field_id)
        return queryset


class InputTextViewSet(ModelViewSet):
    serializer_class = InputTextSerializer
    queryset = UserInputTextValue.objects.all()


class InputAttachmentViewSet(ModelViewSet):
    serializer_class = InputAttachmentSerializer
    queryset = UserInputAttachment.objects.all()


class UserInputViewSet(ModelViewSet):
    serializer_class = UserInputSerializer
    queryset = UserInput.objects.all()
