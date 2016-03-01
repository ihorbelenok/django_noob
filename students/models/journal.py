# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class JournalEntry(models.Model):

    """Journal entry model"""
    year = models.IntegerField(
        verbose_name=u"Рік",
        blank=False,
        null=True)

    month = models.IntegerField(
        verbose_name=u"Місяць",
        blank=False,
        null=True)

    day = models.IntegerField(
        verbose_name=u"День",
        blank=False,
        null=True)

    visited = models.BooleanField(
        default=True,
        verbose_name=u"Відвідав",
        blank=False)

    student_visit = models.ForeignKey('Student',
                                      verbose_name=u'Студент',
                                      blank=False,
                                      null=False,
                                      on_delete=models.CASCADE)

    class Meta(object):
        verbose_name = u'Візит'
        verbose_name_plural = u'Візити'

    def __unicode__(self):
        return u"%s %s @ %d-%d-%d" % (self.student_visit.first_name,
                                      self.student_visit.last_name,
                                      self.year,
                                      self.month,
                                      self.day)
