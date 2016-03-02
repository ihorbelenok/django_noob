# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Exam(models.Model):

    """Exam model"""
    subject = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Предмет")

    examdate = models.DateTimeField(
        blank=False,
        verbose_name=u"Дата і час проведення")

    teacher = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Викладач")

    exam_group = models.ForeignKey('Group',
                                   verbose_name=u'Група',
                                   blank=False,
                                   null=True,)

    class Meta(object):
        verbose_name = u'Іспит'
        verbose_name_plural = u'Іспити'

    def __unicode__(self):
        return u"%s - %s @ %s" % (self.subject,
                                  self.exam_group,
                                  self.examdate)
