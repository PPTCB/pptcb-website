from django.test import TestCase
from .models import Page


class PageSystemUrlTests(TestCase):

    def test_page(self):
        page = Page.objects.create(title='about')
        self.assertEqual(page.system_path, '/about/')

    def test_child_page_of_page(self):
        page_1 = Page.objects.create(title='foo')
        page_2 = Page.objects.create(title='bar', parent=page_1)
        self.assertEqual(page_2.system_path, '/foo/bar/')

    def test_grandchild_page_of_page(self):
        page_1 = Page.objects.create(title='foo')
        page_2 = Page.objects.create(title='bar', parent=page_1)
        page_3 = Page.objects.create(title='baz', parent=page_2)
        self.assertEqual(page_3.system_path, '/foo/bar/baz/')

    def test_home_page(self):
        home_page = Page.objects.create(title='home')
        self.assertEqual(home_page.system_path , '/')

    def test_child_page_of_home(self):
        home_page = Page.objects.create(title='home')
        content_page = Page.objects.create(title='about', parent=home_page)
        self.assertEqual(content_page.system_path , '/about/')