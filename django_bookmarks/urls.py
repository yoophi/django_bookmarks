from django.conf.urls import include, url
from django.contrib import admin

from bookmarks.views import main_page, user_page, logout_page

urlpatterns = [
    url(r'^$', main_page),
    url(r'user/(\w+)', user_page),
    url(r'login/$', 'django.contrib.auth.views.login'),
    url(r'logout/$', logout_page),
    url(r'^admin/', include(admin.site.urls)),
]
