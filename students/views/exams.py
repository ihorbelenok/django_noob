# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.exams import Exam

from django.core.urlresolvers import reverse

from endless_pagination.decorators import page_template
from endless_pagination import utils

from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView, DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button

from django.contrib import messages


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


class ExamAddForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExamAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('exams_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.add_input(Submit('save_button', u'Надіслати'))
        self.helper.add_input(
            Button('cancel_button', u'Скасувати', onclick='window.location.href="{}"'.format(reverse('exams'))))

class ExamAddView(CreateView):
    model = Exam
    template_name = 'students/exams_add_edit.html'
    form_class = ExamAddForm

    def get_success_url(self):
        messages.success(self.request, u"Групу успішно додано!")
        return reverse('exams')

class ExamUpdateForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExamUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('exams_edit', kwargs={'pk': self.instance.id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.add_input(Submit('save_button', u'Надіслати'))
        self.helper.add_input(
            Button('cancel_button', u'Скасувати', onclick='window.location.href="{}"'.format(reverse('exams'))))

class ExamUpdateView(UpdateView):
    model = Exam
    template_name = 'students/exams_add_edit.html'
    form_class = ExamUpdateForm

    def get_success_url(self):
        messages.success(self.request, u"Групу успішно додано!")
        return reverse('exams')


class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'students/exams_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Іспит успішно видалено!")
        return reverse('exams')

