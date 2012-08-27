import PyRSS2Gen as RSS2

from pyramid.response import Response

from kotti import get_settings
from kotti import DBSession
from kotti.resources import get_root
from kotti.resources import Content
from kotti.security import has_permission
from kotti.views.slots import assign_slot
from kotti.views.util import TemplateAPI


def result_items(context, request):
    settings = get_settings()
    content_types = settings.get(
        'kotti_feed.content_types', 'document').split(' ')
    items = DBSession.query(Content).filter(
        Content.type.in_(content_types)).order_by(Content.modification_date)
    context_path = request.resource_path(context)
    return [item for item in items
            if (has_permission('view', item, request) and
                request.resource_path(item).startswith(context_path))]


def rss_items(context, request):
    api = TemplateAPI(context, request)
    items = result_items(context, request)
    return [RSS2.RSSItem(title=item.title,
                         link=api.url(item),
                         description=item.description,
                         guid=RSS2.Guid(api.url(item)),
                         pubDate=item.modification_date,
                         ) for item in items]


def rss_basic_info(context, request):
    settings = get_settings()
    root = get_root()
    api = TemplateAPI(context, request)
    rss_title = settings.get('kotti.site_title') or root.title

    return dict(title=rss_title + ' feed',
                link=api.url(root),
                description=root.description)


def rss_view(context, request):
    rss_info = rss_basic_info(context, request)
    rss_info['items'] = rss_items(context, request)
    rss = RSS2.RSS2(**rss_info)

    return Response(body=rss.to_xml(encoding='utf-8'),
                    content_type='application/rss+xml')


def rss_head_link(context, request):
    rss_info = rss_basic_info(context, request)
    rss_info['rss_link'] = rss_info['link'] + 'rss_view'
    return rss_info


def rss_icon(context, request):
    api = TemplateAPI(context, request)
    return dict(
        rss_url=api.url(context) + 'rss_view',
        icon_url=request.static_url('kotti_feed:static/feed-icon-14x14.png'))


def includeme(config):  # pragma: no cover
    config.add_view(rss_view, name='rss_view', permission='view')

    config.add_view(rss_head_link, name='rss-head-link',
                    renderer='templates/rss-head-link.pt')
    assign_slot('rss-head-link', 'inhead')

    config.add_view(rss_icon, name='rss-icon',
                    renderer='templates/rss-icon.pt')
    assign_slot('rss-icon', 'abovecontent')

    config.add_static_view('static-kotti_feed', 'kotti_feed:static')
