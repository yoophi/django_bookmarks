# -*- coding: utf8 -*-
from django.http import HttpResponse
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
    # output = '''
    # <html>
    # <head><title>%s</title></head>
    # <body>
    # <h1>%s</h1>
    # <p>%s</p>
    # </body>
    # </html>
    # ''' % (
    #     '장고 | 북마크',
    #     '장고북마크에 오신 것을 환영합니다',
    #     '여기에 북마크를 저장하고 공유할 수 있습니다.'
    # )
    #
    return HttpResponse(output)
