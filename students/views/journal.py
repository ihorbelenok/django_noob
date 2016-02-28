# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import datetime
from django.utils import translation
import calendar
import locale
locale.setlocale(locale.LC_ALL, '')


def journal(request):
    students = (
        {'id': 1,
         'first_name': u'Іван',
         'last_name': u'Іваненко', },
        {'id': 2,
         'first_name': u'Петро',
         'last_name': u'Петренко', },
        {'id': 3,
         'first_name': u'Джон',
         'last_name': u'Доу', },
    )
    translation.activate('ua')
    cal = calendar.Calendar(0).itermonthdays2(datetime.now().year,
                                              datetime.now().month)
    days = []
    for i in cal:
        if not i[0] == 0:
            days.append(calendar.day_abbr[i[1]] + ' ' + str(i[0]))

    return render(request,
                  'students/journal.html',
                  {'days': days,
                   'students': students,
                   })
