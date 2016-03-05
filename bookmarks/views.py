# -*- coding: utf8 -*-
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template


def main_page(request):
    template = get_template('main_page.html')
    variables = Context({
        'head_title': '장고 | 북마크',
        'page_title': '장고북마크에 오신 것을 환영합니다',
        'page_body': '여기에 북마크를 저장하고 공유할 수 있습니다.'
    })
    output = template.render(variables)
    return HttpResponse(output)


def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except Exception:
        raise Http404('사용자를 찾을 수 없습니다')

    bookmarks = user.bookmark_set.all()
    template = get_template('user_page.html')
    variables = Context({
        'username': username,
        'bookmarks': bookmarks,
    })
    output = template.render(variables)
    return HttpResponse(output)
