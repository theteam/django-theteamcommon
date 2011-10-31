from django import forms
from django.forms.util import flatatt
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


class PercentageWidget(forms.TextInput):

    def render(self, name, value, attrs=None):
        output = []
        attrs['class'] = 'percent-box'
        output.append('<div class="slide"></div>')
        output.append(super(PercentageWidget,
                            self).render(name, value, attrs))
        output.append(u'%')
        return mark_safe(''.join(output))


class MultipleUrlsWidget(forms.Textarea):

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if isinstance(value, (list, tuple)):
            value = '\r\n'.join(value)
        return mark_safe(u'<textarea%s>%s</textarea>' %
                         (flatatt(final_attrs),
                          conditional_escape(force_unicode(value))))

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)
