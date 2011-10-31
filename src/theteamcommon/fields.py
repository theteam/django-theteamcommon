from django import forms
from django.core.validators import URLValidator
from django.utils.encoding import smart_unicode

from theteamcommon.widgets import MultipleUrlsWidget


class MultipleURLSField(forms.Field):
    """Fakes adding multiple URLS to a TextField
    URLS must be valid and separated by a new line character
    """

    def __init__(self, *args, **kwargs):
        super(MultipleURLSField, self).__init__(*args, **kwargs)
        # define our own widget for this field
        self.widget = MultipleUrlsWidget()

    def to_python(self, value):
        if not value:
            return u''
        elif not isinstance(value, (list, tuple)):
            return smart_unicode(value)
        else:
            return '\r\n'.join(smart_unicode(val) for val in value)

    def clean(self, *args, **kwargs):
        """validates each line is a url"""
        cleaned_data = super(MultipleURLSField, self).clean(*args, **kwargs)
        url_list = cleaned_data.split('\r\n')
        cleaned_list = []
        for url in url_list:
            # TODO clean whitespace
            tmp_url = url.replace('\r', '')
            if tmp_url:
                if not tmp_url.startswith('http'):
                    tmp_url = 'http://%s' % tmp_url
                validator = URLValidator(verify_exists=False)
                validator(tmp_url)
                # if it hasn't rised an exception here it should be clean
                cleaned_list.append(tmp_url)
        return "\r\n".join(cleaned_list)
