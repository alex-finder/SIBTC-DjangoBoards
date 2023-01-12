import unittest

from django.test import TestCase
from django.urls import reverse, resolve

from .views import home


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    @unittest.skip
    def test_home_url_resolves_home_view(self):
        # TODO: fix test_home_url_resolves_home_view (boards.tests.test_views.HomeTests)
        view = resolve('/')
        self.assertEquals(view.func, home)
