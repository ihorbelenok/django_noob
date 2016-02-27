# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import datetime
from django.utils import translation
from calendar import monthrange


def journal(request):
    translation.activate('ua')
    mrange = monthrange(datetime.now().year, datetime.now().month)
    return render(request,
                  'students/journal.html',
                  {'datetime': datetime.now(),
                   'monthrange': range(mrange[0], mrange[1]),
                   })
