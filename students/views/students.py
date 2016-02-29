# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from ..models import Student
from studentsdb.settings import MEDIA_ROOT


# Students views
def students_list(request):
    print MEDIA_ROOT

    students = Student.objects.all()
    return render(request,
                  'students/students_list.html',
                  {'students': students})


def students_add(request):
    return HttpResponse('<h1>Student add form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit student %s</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete student %s</h1>' % sid)
