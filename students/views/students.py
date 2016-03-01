# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.students import Student


# Students views
def students_list(request):
    students = Student.objects.all().order_by('last_name')

    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'card', 'id'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paginate students
    per_page = 3
    total_pages = -(-len(students) // per_page)
    page_string = request.GET.get('page')
    current_page = 1
    try:
        current_page = int(page_string)
    except (ValueError, TypeError):
        # if page not integer - return first page
        current_page = 1
    current_page = max(1, min(total_pages, current_page))
    students = students[(current_page - 1) * per_page:current_page * per_page]
    return render(request,
                  'students/students_list.html',
                  {'students': students,
                   'pages': range(1, total_pages + 1),
                   'current_page': current_page})


def students_add(request):
    return HttpResponse('<h1>Student add form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Edit student %s</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete student %s</h1>' % sid)
