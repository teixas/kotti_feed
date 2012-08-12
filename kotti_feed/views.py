import PyRSS2Gen as RSS2

from pyramid.response import Response

from kotti import get_settings
from kotti import DBSession
from kotti.resources import get_root
from kotti.resources import Content
from kotti.security import has_permission
from kotti.views.util import TemplateAPI


def rss_items(context, request):
    settings = get_settings()
    api = TemplateAPI(context, request)

    content_types = settings.get(
        'kotti_feed.content_types', 'document').split(' ')
    items = DBSession.query(Content).filter(
        Content.type.in_(content_types)).order_by(Content.modification_date)
    return [RSS2.RSSItem(title=item.title,
                         link=api.url(item),
                         description=item.description,
                         guid=RSS2.Guid(api.url(item)),
                         pubDate=item.modification_date,
                         ) for item in items
            if has_permission('view', item, request)]


def rss_view(context, request):
    settings = get_settings()
    root = get_root()
    api = TemplateAPI(context, request)

    rss_title = settings.get('kotti.site_title') or root.title
    items = rss_items(context, request)
    rss = RSS2.RSS2(
        title=rss_title + ' feed',
        link=api.url(root),
        description=root.description,
        items=items,
        )
    return Response(body=rss.to_xml(), content_type='application/rss+xml')


def includeme(config):  # pragma: no cover
    config.add_view(
        rss_view,
        name='rss_view',
        permission='view',
        )
