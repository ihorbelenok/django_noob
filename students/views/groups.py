# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import Group


def groups_list(request):
    groups = Group.objects.all().order_by('title')
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'id'):
        groups = groups.order_by(order_by)
    elif order_by == 'leader':
        groups = groups.order_by("leader__first_name")
    if request.GET.get('reverse', '') == '1':
        groups = groups.reverse()

    #paginate groups
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        #if page not integer - return first page
        groups = paginator.page(1)
    except EmptyPage:
        #if page > num_pages - return last page
        groups = paginator.page(paginator.num_pages)

    return render(request, 'students/groups.html', {"groups": groups})


def groups_add(request):
    return HttpResponse('<h1>Group add form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete group %s</h1>' % gid)
