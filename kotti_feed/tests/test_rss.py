from kotti.testing import DummyRequest
from kotti.testing import UnitTestBase


class TestRSS(UnitTestBase):

    def test_rss_basic_site(self):
        from kotti_feed.views import rss_view
        request = DummyRequest()
        rss = rss_view(request.context, request)
        assert rss.content_type == 'application/rss+xml'
        assert '<channel><title>Welcome to Kotti feed</title>' in rss.body
