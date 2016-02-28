# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


def groups_list(request):
    groups = (
        {'id': 1,
         'name': u'МтМ-21',
         'leader': u'Іваненко Іван', },
        {'id': 2,
         'name': u'МтМ-22',
         'leader': u'Петренко Петро', },
        {'id': 3,
         'name': u'МтМ-23',
         'leader': u'Доу Джон', },
    )
    return render(request, 'students/groups.html', {"groups": groups})


def groups_add(request):
    return HttpResponse('<h1>Group add form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete group %s</h1>' % gid)
