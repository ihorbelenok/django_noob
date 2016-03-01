# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import datetime
from ..models.students import Student
from ..models.journal import JournalEntry
import calendar
import locale
locale.setlocale(locale.LC_ALL, '')


def journal(request):
    day_abbr = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд')
    months = ('Січень', 'Лютий', 'Березень', 'Квітень',
              'Травень', 'Червень', 'Липень', 'Серпень',
              'Вересень', 'Жовтень', 'Листопад', 'Грудень')
    year_string = request.GET.get('year')
    month_string = request.GET.get('month')
    try:
        year = int(year_string)
    except (ValueError, TypeError):
        year = datetime.now().year

    try:
        month = int(month_string)
    except (ValueError, TypeError):
        month = datetime.now().month

    cal = calendar.Calendar(0).itermonthdays2(year,
                                              month)

    days = []
    for i in cal:
        if not i[0] == 0:
            days.append(day_abbr[i[1]] + ' ' + str(i[0]))

    students = Student.objects.all()
    entries = JournalEntry.objects.filter(year=year, month=month)

    journaldata = []

    # paginate journal
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

    for st in students:
        visitation_array = [False for i in days]
        for day in range(len(days)):
            visitation = entries.filter(student_visit=st, day=day + 1)
            if visitation.count() != 0:
                visitation_array[day] = visitation[0].visited
        journaldata.append((st.id,
                            st.first_name + ' ' + st.last_name,
                            visitation_array))

    return render(request,
                  'students/journal.html',
                  {'days': days,
                   'journaldata': journaldata,
                   'year': year,
                   'month': month,
                   'monthyear': months[month-1]+' '+str(year),
                   'pages': range(1, total_pages + 1),
                   'current_page': current_page
                   })
