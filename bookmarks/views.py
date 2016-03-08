# -*- coding: utf8 -*-
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from bookmarks.forms import RegistrationForm, BookmarkSaveForm
from bookmarks.models import Link, Bookmark, Tag


def main_page(request):
    return render_to_response(
        'main_page.html',
        RequestContext(request)
    )


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.order_by('-id')

    variables = RequestContext(request, {
        'username': username,
        'bookmarks': bookmarks,
        'show_tags': True,
    })
    return render_to_response('user_page.html', variables)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('registration/register.html', variables)


@login_required(login_url='/login/')
def bookmark_save_page(request):
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            # URL이 있으면 가져오고 없으면 새로 저장합니다.
            link, _ = Link.objects.get_or_create(
                url=form.cleaned_data['url']
            )

            # 북마크가 있으면 가져오고 없으면 새로 저장합니다.
            bookmark, created = Bookmark.objects.get_or_create(
                user=request.user,
                link=link
            )

            # 북마크 제목을 수정합니다.
            bookmark.title = form.cleaned_data['title']

            # 북마크를 수정한 경우에는 이전에 입력된 모든 태그를 지웁니다
            if not created:
                bookmark.tag_set.clear()

            # 태그 목록을 새로 만듭니다.
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                bookmark.tag_set.add(tag)

            bookmark.save()
            return HttpResponseRedirect(
                '/user/%s/' % request.user.username
            )
    else:
        form = BookmarkSaveForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('bookmark_save.html', variables)
