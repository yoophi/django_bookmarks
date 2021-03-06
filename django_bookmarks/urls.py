# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from bookmarks.feed import RecentBookmarks, UserBookmarks
from bookmarks.views import main_page, user_page, logout_page, register_page, bookmark_save_page, tag_page, \
    tag_cloud_page, search_page, ajax_tag_autocomplete, bookmark_vote_page, popular_page, bookmark_page, friends_page, \
    friend_add, friend_accept, friend_invite

urlpatterns = [
    # 북마크 조회
    url(r'^$', main_page),
    url(r'^popular/$', popular_page),
    url(r'^user/(\w+)', user_page),
    url(r'^tag/([^\s]+)/$', tag_page),
    url(r'^tag/$', tag_cloud_page),
    url(r'^search/$', search_page),
    url(r'^bookmark/(\d+)/$', bookmark_page),

    # 친구들
    url(r'^friends/(\w+)/$', friends_page),
    url(r'^friend/add/$', friend_add),
    url(r'^friend/invite/$', friend_invite),
    url(r'^friend/accept/(\w+)/$', friend_accept),

    # 세션 관리
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', logout_page),
    url(r'^register/$', register_page),
    url(r'^register/success/$',
        TemplateView.as_view(template_name='registration/register_success.html'),
        name='register_success'
        ),

    # 계정 관리
    url(r'^save/$', bookmark_save_page),
    url(r'^vote/$', bookmark_vote_page),

    # AJAX
    url(r'^ajax/tag/autocomplete/$', ajax_tag_autocomplete),

    # 관리 페이지
    url(r'^admin/', include(admin.site.urls)),

    # 댓글
    url(r'^comments/', include('django_comments.urls')),

    # Feeds
    url(r'^feeds/recent/$', RecentBookmarks()),
    url(r'^feeds/user/(?P<username>.*)/$', UserBookmarks()),
]
