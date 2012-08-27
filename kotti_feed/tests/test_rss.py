from pyramid.threadlocal import get_current_registry

from kotti.testing import DummyRequest
from kotti.testing import UnitTestBase


def settings():
    return get_current_registry().settings


class TestRSS(UnitTestBase):

    def test_rss_basic_site(self):
        from kotti_feed.views import rss_view

        request = DummyRequest()
        rss = rss_view(request.context, request)
        assert rss.content_type == 'application/rss+xml'
        assert '<channel><title>Welcome to Kotti feed</title>' in rss.body


class TestRSSHeadLink(UnitTestBase):
    def test_rss_head_link(self):
        from kotti_feed.views import rss_head_link

        request = DummyRequest()
        head_link = rss_head_link(request.context, request)
        assert 'title' in head_link
        assert 'rss_link' in head_link
        assert head_link['rss_link'] == 'http://example.com/rss_view'


class TestRSSIcon(UnitTestBase):
    def test_rss_icon_at_root(self):
        from kotti_feed.views import rss_icon

        request = DummyRequest()
        request.static_url = lambda url: url
        icon = rss_icon(request.context, request)
        assert 'rss_url' in icon
        assert 'icon_url' in icon
        assert icon['rss_url'] == 'http://example.com/rss_view'

    def test_rss_icon_at_child(self):
        from kotti.resources import get_root
        from kotti.resources import Document
        from kotti_feed.views import rss_icon

        request = DummyRequest()
        request.static_url = lambda url: url
        root = get_root()
        child = root['child'] = Document(u'Child')

        icon = rss_icon(child, request)
        assert 'rss_url' in icon
        assert 'icon_url' in icon
        assert icon['rss_url'] == 'http://example.com/child/rss_view'


class TestRSSItems(UnitTestBase):
    def test_default_content_type_items(self):
        from kotti_feed.views import rss_items

        request = DummyRequest()
        items = rss_items(request.context, request)
        assert len(items) == 1
        assert items[0].link == 'http://example.com/'
        assert items[0].description == \
            u'Congratulations! You have successfully installed Kotti.'

    def test_document_or_image_type_items(self):
        from kotti_feed.views import rss_items

        request = DummyRequest()
        settings()['kotti_feed.content_types'] = 'document image'
        items = rss_items(request.context, request)
        assert len(items) == 1
        assert items[0].link == 'http://example.com/'
        assert items[0].description == \
            u'Congratulations! You have successfully installed Kotti.'

    def test_image_type_items(self):
        from kotti_feed.views import rss_items

        request = DummyRequest()
        settings()['kotti_feed.content_types'] = 'image'
        items = rss_items(request.context, request)
        assert len(items) == 0

    def test_special_chars_in_feed(self):
        from kotti_feed.views import rss_view
        from kotti.resources import Document, get_root

        root = get_root()
        request = DummyRequest()
        settings()['kotti_feed.content_types'] = 'document image'
        root['doc1'] = Document(title=u'L\xc3\xb6vely Document')
        feed = rss_view(request.context, request)
        assert u'L\xc3\xb6vely Document' in feed.text
        assert u'encoding="utf-8"' in feed.text


class TestRSSContext(UnitTestBase):

    def test_root_rss_feed(self):
        from kotti.resources import get_root
        from kotti_feed.views import rss_items
        request = DummyRequest()

        root = get_root()
        items = rss_items(root, request)
        assert len(items) == 1
        assert items[0].link == 'http://example.com/'

    def test_child_rss_feed(self):
        from kotti.resources import get_root
        from kotti.resources import Document
        from kotti_feed.views import rss_items
        request = DummyRequest()

        root = get_root()
        child = root['child'] = Document(u'Child')
        items = rss_items(root, request)
        assert len(items) == 2
        assert items[0].link == 'http://example.com/'
        assert items[1].link == 'http://example.com/child/'

        items = rss_items(child, request)
        assert len(items) == 1
        assert items[0].link == 'http://example.com/child/'
