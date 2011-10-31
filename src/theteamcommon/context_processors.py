from django.conf import settings


def common_variables(request):
    extra_context = {}
    extra_context['STATIC_URL'] = settings.STATIC_URL
    return extra_context
