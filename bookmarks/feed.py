# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
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


class UserBookmarks(Feed):
    def get_object(self, request, *args, **kwargs):
        return User.objects.get(username=(kwargs.get('username')))

    def item_title(self, item):
        return u'장고 북마크 | %s가 등록한 북마크' % item.user.username

    def link(self, user):
        return '/feeds/user/%s/' % user.username

    def item_description(self, item):
        return u'장고 북마크 서비스를 통해서 %s가 등록한 북마크' % item.user.username

    def items(self, user):
        return user.bookmark_set.order_by('-id')[:10]
