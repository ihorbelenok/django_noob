# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


# Students views
def students_list(request):
    students = (
        {'id': 1,
         'first_name': u'Іван',
         'last_name': u'Іваненко',
         'card': 235,
         'image': 'img/face_angel.png'},
        {'id': 2,
         'first_name': u'Петро',
         'last_name': u'Петренко',
         'card': 2123,
         'image': 'img/face_cool.png'},
        {'id': 3,
         'first_name': u'Джон',
         'last_name': u'Доу',
         'card': 123,
         'image': 'img/face_devilish.png'},
    )
    return render(request,
                  'students/students_list.html',
                  {'students': students})


def students_add(request):
    return HttpResponse('<h1>Student add form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit student %s</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete student %s</h1>' % sid)


# Groups views
def groups_list(request):
    return render(request, 'students/groups.html', {})


def groups_add(request):
    return HttpResponse('<h1>Group add form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Edit group %s</h1>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Delete group %s</h1>' % gid)
