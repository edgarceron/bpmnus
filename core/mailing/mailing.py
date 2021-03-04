from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags

def send_confirmacion(to, template, context):
    subject = "Reserva para " + context["motivo"]
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    return send_mail(
        subject='Su cita en concesionario caribe renault',
        message=plain_message,
        html_message=html_message,
        from_email='Concesionario Caribe Renault<notificaciones@caribecali.com>',
        recipient_list=[to,],
        fail_silently=False
    )
