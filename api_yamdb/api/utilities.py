from django.conf import settings
from django.core.mail import send_mail


def send_confirm_code(email, confirm_code):
    send_mail(
        subject='Confirmation code YaMDb',
        message=f'Ваш код подтверждения: {confirm_code}',
        from_email=settings.DOMAIN_NAME,
        recipient_list=(email,),
        fail_silently=False)
