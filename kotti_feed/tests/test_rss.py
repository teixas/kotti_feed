from pyramid.threadlocal import get_current_registry

from kotti.testing import DummyRequest
from kotti.testing import FunctionalTestBase
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


class TestRSSContext(FunctionalTestBase):

    def setUp(self, **kwargs):
        settings = {'kotti.configurators': 'kotti_feed.kotti_configure'}
        super(TestRSSContext, self).setUp(**settings)

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
        assert items[1].link == 'http://example.com/chid/'

        items = rss_items(child, request)
        assert len(items) == 1
        assert items[0].link == 'http://example.com/child/'
