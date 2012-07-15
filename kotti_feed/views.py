import PyRSS2Gen as RSS2

from pyramid.response import Response

from kotti import get_settings
from kotti import DBSession
from kotti.resources import get_root
from kotti.resources import Content
from kotti.views.util import TemplateAPI


def rss_view(context, request):
    root = get_root()
    api = TemplateAPI(context, request)

    items = DBSession.query(Content).filter(
        Content.type == 'document').order_by(Content.modification_date)
    rss_items = [RSS2.RSSItem(title=item.title,
                              link=api.url(item),
                              description=item.description,
                              guid=RSS2.Guid(api.url(item)),
                              pubDate=item.modification_date,
                              ) for item in items]
    rss_title = get_settings().get('kotti.site_title') or root.title
    rss = RSS2.RSS2(
        title=rss_title + ' feed',
        link=api.url(root),
        description=root.description,
        items=rss_items,
        )
    return Response(body=rss.to_xml(), content_type='application/rss+xml')


def includeme(config):  # pragma: no cover
    config.add_view(
        rss_view,
        name='rss_view',
        permission='view',
        )
