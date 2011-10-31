import re

from django.conf import settings
from django.db.models import get_model
from decimal import Decimal


def get_attachment_type(filename):
    """Guess the attachment type from the filename"""
    attachment_list = {'pdf': 'pdf',
                       'txt': 'txt',
                       'doc': 'doc',
                       'ptt': 'ptt',
                       'xls': 'xls',
                       }
    name_list = filename.split('.')
    extension = name_list[-1].lower()
    if extension in attachment_list:
        return attachment_list[extension]
    return u'unknown'


def get_file_size(file_object):
    """Returns the size in MB or KB from an
    object file"""
    try:
        size = Decimal(str(file_object.size))
    except OSError:
        # TODO: log this error
        size = Decimal(0)
    kb = size / 1024
    # save KB or MB according to size
    if kb < 1024:
        return '%sKB' % round(kb, 2)
    mb = kb / 1024
    return '%sMB' % round(mb, 2)


def import_model(relation):
    """Returns a model class from a string reference
    ``app_label.ModelName``
    """
    app_label, model_name = relation.split(".")
    return get_model(app_label, model_name, True)


def fix_url(url):
    """Appends http:// protocol if missing from a given url"""
    if not url.startswith('http'):
        url = 'http://%s' % url
    return url


def parse_input_fields(response):
    """Helper to get the fields value from the response
    """
    input_re = re.compile('name="([^"]+)" value="([^"]+)"')
    input_re2 = re.compile("name='([^']+)' value='([^']+)'")
    fields = {}

    def grab(m):
        # populate the fields
        fields[m.group(1)] = m.group(2)
        return
    input_re.sub(grab, response)
    input_re2.sub(grab, response)
    return fields


def get_format_url():
    """returns a list of supported formats"""
    keys = settings.CONTENT_FORMAT.keys()
    supported_formats = '|'.join(keys)
    return "\.(?P<format>(" + supported_formats + "))"
format_url = get_format_url()
