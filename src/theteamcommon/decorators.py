from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404


def render_response(func):
    """Render to response"""
    def inner(request, *args, **kwargs):
        result = func(request, *args, **kwargs)
        if isinstance(result, HttpResponse):
            return result
        template, dictionary = result
        return render_to_response(template, dictionary,
                                  RequestContext(request))
    return inner


def accepted_format(func):
    """Validates we support the given response
    and adds the content type to the specified in the
    ``CONTENT_FORMAT`` setting
    """
    def wrapper(request, *args, **kwargs):
        # the request is explicitly asking for a format
        response_type = None
        if 'format' in kwargs:
            request_format = kwargs['format']
            if request_format in settings.CONTENT_FORMAT:
                response_type = settings.CONTENT_FORMAT[request_format]
            else:
                # invalid format request
                raise Http404
        response = func(request, *args, **kwargs)
        # change content_type according to settings
        if response_type:
            response['Content-Type'] = response_type
        return response
    return wrapper
