# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.groups import Group


def groups_list(request):
    groups = Group.objects.all().order_by('title')
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'id'):
        groups = groups.order_by(order_by)
    elif order_by == 'leader':
        groups = groups.order_by("leader__first_name")
    if request.GET.get('reverse', '') == '1':
        groups = groups.reverse()

    # paginate groups
    per_page = 3
    total_pages = -(-len(groups) // per_page)
    page_string = request.GET.get('page')
    current_page = 1
    try:
        current_page = int(page_string)
    except (ValueError, TypeError):
        # if page not integer - return first page
        current_page = 1
    current_page = max(1, min(total_pages, current_page))
    groups = groups[(current_page - 1) * per_page:current_page * per_page]
    return render(request,
                  'students/groups.html',
                  {"groups": groups,
                   'pages': range(1, total_pages + 1),
                   'pageindex': (current_page - 1) * per_page})


def groups_add(request):
    return HttpResponse('<h1>Group add form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete group %s</h1>' % gid)
