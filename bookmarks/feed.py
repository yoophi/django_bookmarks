# -*- coding: utf8 -*-
from django.contrib.syndication.views import Feed

from bookmarks.models import Bookmark


class RecentBookmarks(Feed):
    title = u'장고 북마크 | 최신 북마크'
    link = '/feeds/recent/'
    description = u'장고 북마크 서비스를 통해서 등록된 북마크'

    title_template = 'feeds/recent_title.html'
    description_template = 'feeds/recent_description.html'

    def items(self):
        return Bookmark.objects.order_by('-id')[:10]
