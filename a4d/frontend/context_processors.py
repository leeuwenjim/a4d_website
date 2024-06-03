from django.conf import settings

def contact_email_context(request):
    return {'CONTACT_EMAIL': settings.CONTACT_MAIL}
def statics_version_context(request):
    return {'STATICS_VERSION': settings.STATICS_VERSION}
