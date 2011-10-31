import re
from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter

register = template.Library()

CLASS_PATTERN = re.compile(r'\bclass="[\w\d]*"')


def cssclass(value, arg):
    """Replace the attribute css class for Field 'value' with 'arg'.
    """
    value.field.widget.attrs.update({'class': arg})
    return value
register.filter('cssclass', cssclass)


def attr(value, arg):
    """Add an attribute to a form field
    {{ field|attr:"name=blah"|attr:"whatever=blah" }}
    """
    args = arg.split('=')
    value.field.widget.attrs.update({args[0]: args[1]})
    return value
register.filter('attr', attr)


@register.filter
def empty_label(value, arg):
    """
    Set the text for the initial option in a ModelChoiceField
    """
    value.field.empty_label = arg
    return value


@register.filter
@stringfilter
def truncchars(value, length):
    if len(value) > length:
        return "%s..." % value[:length]
    return value


@register.simple_tag
def get_admin_url(context, item):
    """Returns the URL for the current admin object"""
    admin_key = u'admin:%s_%s_change' % (item._meta.app_label,
                                         item._meta.module_name)
    return reverse(admin_key, args=[item.id, ])
