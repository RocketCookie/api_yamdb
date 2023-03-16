from django.core.mail import send_mail


def send_confirm_code(email, confirm_code):
    send_mail(
        subject='Код подтверждения YaMDb',
        message=f'Ваш код подтверждения: {confirm_code}',
        from_email='no_reply@yamdb.com',
        recipient_list=(email,),
        fail_silently=False)
