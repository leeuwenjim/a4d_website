from django.conf import settings

def contact_email_context(request):
    return {'CONTACT_EMAIL': settings.CONTACT_MAIL}
