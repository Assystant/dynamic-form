from rest_framework.routers import SimpleRouter
from .views import *


router = SimpleRouter()

router.register(r'template', TemplateViewSet, basename='template')
router.register(r'field', FieldViewSet, basename='field')
router.register(r'field-validation', FieldValidationViewSet, basename='field-validation')
router.register(r'field-option', FieldOptionViewSet, basename='field-option')
router.register(r'input-text', InputTextViewSet, basename='input-text')
router.register(r'input-attachment', InputAttachmentViewSet, basename='input-attachment')
router.register(r'user-input', UserInputViewSet, basename='user-input')

urlpatterns = router.urls