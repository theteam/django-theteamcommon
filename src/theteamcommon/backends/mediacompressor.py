from django.conf import settings
from mediasync import JS_MIMETYPES, CSS_MIMETYPES
import os
from subprocess import Popen, PIPE


def _yui_path(settings):
    if not hasattr(settings, 'MEDIASYNC'):
        return None
    path = settings.MEDIASYNC.get('YUI_COMPRESSOR_PATH', None)
    if path:
        path = os.path.realpath(os.path.expanduser(path))
    return path


def _uglify_path(settings):
    if not hasattr(settings, 'MEDIASYNC'):
        return None
    path = settings.MEDIASYNC.get('UGLIFY_COMPRESSOR_PATH', None)
    if path:
        path = os.path.realpath(os.path.expanduser(path))
    return path


def css_minifier(filedata, content_type, remote_path, is_active):
    is_css = (content_type in CSS_MIMETYPES or \
              remote_path.lower().endswith('.css'))
    yui_path = _yui_path(settings)
    if is_css and yui_path and is_active:
        proc = Popen(['java', '-jar', yui_path, '--type', 'css'], stdout=PIPE,
                     stderr=PIPE, stdin=PIPE)
        stdout, stderr = proc.communicate(input=filedata)
        return str(stdout)


def js_minifier(filedata, content_type, remote_path, is_active):
    is_js = (content_type in JS_MIMETYPES or \
             remote_path.lower().endswith('.js'))
    uglify_path = _uglify_path(settings)
    if is_js and uglify_path and is_active:
        proc = Popen([uglify_path, '--unsafe'], stdout=PIPE,
                     stderr=PIPE, stdin=PIPE)
        stdout, stderr = proc.communicate(input=filedata)
        return str(stdout)
