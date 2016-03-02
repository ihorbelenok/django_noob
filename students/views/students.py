# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.students import Student
from endless_pagination.decorators import page_template
from endless_pagination import utils


@page_template('students/students_page.html')
def students_list(request,
                  template='students/students_list.html',
                  page_template='students/students_page.html',
                  extra_context=None):
    students = Student.objects.all().order_by('last_name')

    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'card', 'id'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    context = {'students': students,
               'page_template': page_template,
               'start_id': (utils.get_page_number_from_request(request)-1)*3,
               'per_page': 3}

    if extra_context is not None:
        context.update(extra_context)
    if request.is_ajax():
        template = page_template

    return render(request, template, context)


def students_add(request):
    return HttpResponse('<h1>Student add form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit student %s</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete student %s</h1>' % sid)
