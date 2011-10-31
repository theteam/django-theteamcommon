from django.conf import settings
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse


# Prevent interactive question about wanting a superuser created.
signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser')


# Create our own test user automatically.
def create_testuser(app, created_models, verbosity, **kwargs):
    username = settings.TEST_USERNAME
    password = settings.TEST_PASSWORD
    if not settings.DEBUG:
        return
    try:
        auth_models.User.objects.get(username=username)
    except auth_models.User.DoesNotExist:
        print '*' * 80
        print 'Creating test user -- login: %s, password: %s' % (username,
                                                                 password)
        print '*' * 80
        data = {'username': username,
                'email': settings.TEST_EMAIL,
                'password': password,
                }
        super_user = auth_models.User.objects.create_superuser(**data)
        assert super_user
        super_user.first_name = 'Team'
        super_user.last_name = 'Digital'
        super_user.save()
    else:
        print 'User already exists.'


if hasattr(settings, 'CREATE_TEST_USER') and settings.CREATE_TEST_USER:
    signals.post_syncdb.connect(create_testuser,
                                sender=auth_models,
                                dispatch_uid='theteamcommon.models.create_testuser')


class SortableModel(models.Model):
    """Adds the ability to be sorted in the admin
    """
    order = models.IntegerField(blank=True, null=True, default=0,
                                editable=False)

    class Meta:
        abstract = True

    def order_link(self):
        model_type_id = ContentType.objects.get_for_model(self.__class__).id
        kwargs = {"model_type_id": model_type_id}
        url = reverse("admin_order", kwargs=kwargs)
        return '<a href="%s" class="order_link">%s</a>' % \
            (url, str(self.pk) or '')
    order_link.allow_tags = True
    order_link.short_description = 'Order'
