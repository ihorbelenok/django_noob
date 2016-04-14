# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.students import Student
from ..models.groups import Group
from endless_pagination.decorators import page_template
from endless_pagination import utils
from datetime import datetime
from django.core.urlresolvers import reverse


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
               'start_id': (utils.get_page_number_from_request(request) - 1) * 3,
               'per_page': 10}

    if extra_context is not None:
        context.update(extra_context)
    if request.is_ajax():
        template = page_template

    return render(request, template, context)


def students_add(request):
    if request.method == "POST":
        if request.POST.get('add_button') is not None:
            errors = {}

            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validating user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Імʼя є обовʼязковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обовʼязковим"
            else:
                data['last_name'] = last_name

            birth_date = request.POST.get('birth_date', '').strip()
            if not birth_date:
                errors['birth_date'] = u"Дата народження є обовʼязковою"
            else:
              try:
                datetime.strptime(birth_date, '%Y-%m-%d')
              except Exception:
                errors['birth_date'] = u"Введіть коректний формат дати (напр. 1987-12-30)"
              else:
                data['birth_date'] = birth_date

            card = request.POST.get('card', '').strip()
            if not card:
                errors['card'] = u"Номер білета є обовʼязковим"
            else:
                data['card'] = card

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Група є обовʼязковою"
            else:
              groups = Group.objects.filter(pk=student_group)
              if len(groups) != 1:
                errors['student_group'] = u"Оберіть коректну групу"
              else:
                data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo

            if not errors:
                student = Student(**data)
                student.save()
                return HttpResponseRedirect(u'%s?status_message=Студента успішно додано!' % reverse('home'))
            else:
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u'%s?status_message=Додавання студента скасовано!' % reverse('home'))
    else:
        return render(request, 'students/students_add.html',
                      {'groups': Group.objects.all().order_by('title')})


def students_edit(request, sid):
    return HttpResponse('<h1>Edit student %s</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete student %s</h1>' % sid)
