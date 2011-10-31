from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.views import login
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse


def error_view(request):
    assert False, request


def error_handler(request):
    response = render_to_response('500.html', {},
                                  RequestContext(request))
    response.status_code = 500
    return response


def not_found_handler(request):
    response = render_to_response('404.html', {},
                                  RequestContext(request))
    response.status_code = 404
    return response


def login_wrapper(request, *args, **kwargs):
    response = login(request, *args, **kwargs)
    if request.user.is_authenticated() and request.method == 'POST':
        if request.POST.get('remember_me'):
            # ~ 6 months
            expiry_time = 60 * 60 * 24 * 30 * 6
            request.session.set_expiry(expiry_time)
        else:
            request.session.set_expiry(0)
        # force save
        request.session.modified = True
    return response


def order(request, model_type_id=None):
    """Reorders the given ``model_type_id`` with the passed ids via POST
    """
    if not request.is_ajax() or not request.method == "POST":
        return HttpResponse("BAD")
    try:
        indexes = request.POST.get('indexes', []).split(",")
        klass = ContentType.objects.get(id=model_type_id).model_class()
        order_field = getattr(klass, 'order_field', 'order')
        objects_dict = dict([(obj.pk, obj) \
                             for obj in klass.objects.filter(pk__in=indexes)])
        min_index = min(objects_dict.values(),
                        key=lambda x: getattr(x, order_field))
        min_index = getattr(min_index, order_field) or 0
        for index in indexes:
            obj = objects_dict[int(index)]
            setattr(obj, order_field, min_index)
            obj.save()
            min_index += 1
    except IndexError:
        pass
    except klass.DoesNotExist:
        pass
    except AttributeError:
        pass
    return HttpResponse()
