# -*- coding: utf8 -*-
import os

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from bookmarks.views import main_page, user_page, logout_page, register_page, bookmark_save_page

site_media = os.path.join(os.path.dirname(__file__), 'site_media')
urlpatterns = [
    # 북마크 조회
    url(r'^$', main_page),
    url(r'^user/(\w+)', user_page),

    # 세션 관리
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^register/$', register_page),
    url(r'^register/success/$',
        TemplateView.as_view(template_name='registration/register_success.html'),
        name='register_success'
        ),

    # 정적 파일
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media}),

    # 계정 관리
    url(r'^save/$', bookmark_save_page),

    # 관리 페이지
    url(r'^admin/', include(admin.site.urls)),
]
