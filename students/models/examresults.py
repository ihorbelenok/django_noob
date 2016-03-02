# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Examresult(models.Model):

    """Examresult model"""
    result_exam = models.ForeignKey('Exam',
                                    verbose_name=u'Іспит',
                                    blank=False,
                                    null=True,)

    result_student = models.ForeignKey('Student',
                                       verbose_name=u'Студент',
                                       blank=False,
                                       null=True,)

    mark = models.CharField(max_length=256,
                            blank=False,
                            verbose_name=u"Оцінка")

    class Meta(object):
        verbose_name = u'Оцінка'
        verbose_name_plural = u'Оцінки'

    def __unicode__(self):
        return u"%s - %s" % (self.result_student,
                             self.result_exam.subject,)
