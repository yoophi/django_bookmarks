# -*- coding: utf8 -*-
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from bookmarks.forms import RegistrationForm, BookmarkSaveForm, SearchForm
from bookmarks.models import Link, Bookmark, Tag, SharedBookmark


def main_page(request):
    shared_bookmarks = SharedBookmark.objects.order_by('-date')[:10]
    variables = RequestContext(request, {
        'shared_bookmarks': shared_bookmarks
    })
    return render_to_response('main_page.html', variables )


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.order_by('-id')

    variables = RequestContext(request, {
        'username': username,
        'bookmarks': bookmarks,
        'show_edit': True,
        'show_tags': username == request.user.username,
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
    ajax = 'ajax' in request.GET
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            bookmark = _bookmark_save(request, form)
            if ajax:
                variables = RequestContext(request, {
                    'bookmarks': [bookmark],
                    'show_edit': True,
                    'show_tags': True,
                })
                return render_to_response('bookmark_list.html', variables)
            else:
                return HttpResponseRedirect(
                    '/user/%s/' % request.user.username
                )
        else:
            if ajax:
                return HttpResponse('failure')

    elif 'url' in request.GET:
        url = request.GET['url']
        title = ''
        tags = ''
        try:
            link = Link.objects.get(url=url)
            bookmark = Bookmark.objects.get(
                link=link,
                user=request.user,
            )
            title = bookmark.title
            tags = ' '.join(
                [tag.name for tag in bookmark.tag_set.all()]
            )
        except ObjectDoesNotExist:
            pass

        form = BookmarkSaveForm({
            'url': url,
            'title': title,
            'tags': tags,
        })
    else:
        form = BookmarkSaveForm()

    variables = RequestContext(request, {
        'form': form
    })
    if ajax:
        return render_to_response('bookmark_save_form.html', variables)
    else:
        return render_to_response('bookmark_save.html', variables)


def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    bookmarks = tag.bookmarks.order_by('-id')
    variables = RequestContext(request, {
        'bookmarks': bookmarks,
        'tag_name': tag_name,
        'show_tags': True,
        'show_user': True,
    })

    return render_to_response('tag_page.html', variables)


def tag_cloud_page(request):
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('name')

    min_count = max_count = tags[0].bookmarks.count()
    for tag in tags:
        tag.count = tag.bookmarks.count()
        if tag.count < min_count:
            min_count = tag.count
        if max_count < tag.count:
            max_count = tag.count

    range = float(max_count - min_count)
    if range == 0.0:
        range = 1.0

    for tag in tags:
        tag.weight = int(
            MAX_WEIGHT * (tag.count - min_count) / range
        )
    variables = RequestContext(request, {
        'tags': tags
    })
    return render_to_response('tag_cloud_page.html', variables)


def search_page(request):
    form = SearchForm()
    bookmarks = []
    show_results = False
    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query': query})
            bookmarks = Bookmark.objects.filter(title__icontains=query)[:10]

    variables = RequestContext(request, {
        'bookmarks': bookmarks,
        'form': form,
        'show_results': show_results,
        'show_tags': True,
        'show_user': True,
    })
    if request.is_ajax():
        return render_to_response('bookmark_list.html', variables)
    else:
        return render_to_response('search.html', variables)


def _bookmark_save(request, form):
    # 링크를 새로 만들거나 가져옵니다.
    link, _ = Link.objects.get_or_create(url=form.cleaned_data['url'])

    # 북마크를 새로 만들거나 가져옵니다.
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        link=link,
    )

    # 북마크 제목을 수정합니다.
    bookmark.title = form.cleaned_data['title']

    # 북마크가 수정된 경우 예전 태그들을 제거합니다.
    if not created:
        bookmark.tag_set.clear()

    # 새로운 태그를 입력합니다.
    tag_names = form.cleaned_data['tags'].split()
    for tag_name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        bookmark.tag_set.add(tag)

    # 첫 페이지에서 공유하도록 설정합니다
    if form.cleaned_data['share']:
        shared_bookmark, created = SharedBookmark.objects.get_or_create(bookmark=bookmark)
        if created:
            shared_bookmark.users_voted.add(request.user)
            shared_bookmark.save()

    # 북마크를 저장하고 다시 북마크를 반환합니다
    bookmark.save()
    return bookmark


def ajax_tag_autocomplete(request):
    if 'q' in request.GET:
        tags = Tag.objects.filter(name__istartswith=request.GET['q'])[:10]
        return HttpResponse('\n'.join([tag.name for tag in tags]))
    return HttpResponse()
