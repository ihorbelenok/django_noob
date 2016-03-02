# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.examresults import Examresult


def examresults_list(request, template='students/examresults.html',):
    examresults = Examresult.objects.all().order_by(
        'result_student__last_name', 'result_student__first_name')

    order_by = request.GET.get('order_by', '')
    if order_by == 'student':
        examresults = examresults.order_by('result_student__last_name',
                                           'result_student__first_name')
    elif order_by == 'date':
        examresults = examresults.order_by('result_exam__examdate')
    elif order_by == 'subj':
        examresults = examresults.order_by('result_exam__subject')
    elif order_by == 'teacher':
        examresults = examresults.order_by('result_exam__teacher')
    elif order_by == 'mark':
        examresults = examresults.order_by('mark')
    if request.GET.get('reverse', '') == '1':
        examresults = examresults.reverse()

    context = {'examresults': examresults}
    return render(request, template, context)


def examresults_add(request):
    return HttpResponse('<h1>Examresults add form</h1>')


def examresults_edit(request, rid):
    return HttpResponse('<h1>Edit examresult %s</h1>' % rid)


def examresults_delete(request, rid):
    return HttpResponse('<h1>Delete examresult %s</h1>' % rid)
