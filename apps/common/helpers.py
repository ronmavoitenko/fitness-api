from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from apps.user.models import User
import random

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Enjoy",
    ),
    public=True,
    permission_classes=[AllowAny],
)


def send_notification(recipients, subject, message):
    from_email = settings.EMAIL_HOST_USER
    if not isinstance(recipients, (list, tuple)):
        recipients = [recipients]
    send_mail(subject, message, from_email, recipients, fail_silently=True)


def generate_code(length=6):
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    secret_code = random.randint(range_start, range_end)
    return secret_code
