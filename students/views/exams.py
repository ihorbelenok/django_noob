# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.exams import Exam


def exams_list(request, template='students/exams.html',):
    exams = Exam.objects.all().order_by('examdate')

    order_by = request.GET.get('order_by', '')
    if order_by in ('subject', 'examdate', 'teacher', 'id', 'exam_group'):
        if order_by == 'exam_group':
            exams = exams.order_by('exam_group__title')
        else:
            exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()

    context = {'exams': exams}
    return render(request, template, context)


def exams_add(request):
    return HttpResponse('<h1>Exams add form</h1>')


def exams_edit(request, eid):
    return HttpResponse('<h1>Edit exam %s</h1>' % eid)


def exams_delete(request, eid):
    return HttpResponse('<h1>Delete exam %s</h1>' % eid)
