# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.groups import Group
from endless_pagination.decorators import page_template
from endless_pagination import utils


@page_template('students/groups_page.html')
def groups_list(request,
                template='students/groups.html',
                page_template='students/groups_page.html',
                extra_context=None):
    groups = Group.objects.all().order_by('title')
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'id'):
        groups = groups.order_by(order_by)
    elif order_by == 'leader':
        groups = groups.order_by("leader__first_name")
    if request.GET.get('reverse', '') == '1':
        groups = groups.reverse()

    context = {"groups": groups,
               'page_template': page_template,
               'start_id': (utils.get_page_number_from_request(request)-1)*3,
               'per_page': 3}

    if extra_context is not None:
        context.update(extra_context)
    if request.is_ajax():
        template = page_template

    return render(request,
                  template,
                  context)


def groups_add(request):
    return HttpResponse('<h1>Group add form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete group %s</h1>' % gid)
