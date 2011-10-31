from django.core.urlresolvers import reverse
from django.test import TestCase


class TeamCommonTests(TestCase):

    fixtures = ['test/admin-views-users.xml']

    def setUp(self):
        """Actions to be performed on each test"""
        self.client.login(username='super', password='secret')

    def tearDown(self):
        self.client.logout()

    def test_admin_index(self):
        """Simple text for the django client"""
        admin_url = reverse('admin:index')
        response = self.client.get(admin_url)
