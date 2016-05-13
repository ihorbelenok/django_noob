# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from ..models.exams import Exam
from ..models.groups import Group

from django.core.urlresolvers import reverse

from endless_pagination.decorators import page_template
from endless_pagination import utils

from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView, DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button

from django.contrib import messages
from datetime import datetime


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


def exam_add(request):
    groups = Group.objects.all()
    data = {}
    errors = {}
    if request.method == "POST":
        if request.POST.get('add_button') is not None:
            subject = request.POST.get('subject', '').strip()
            if not subject:
                errors['subject'] = u"Назва предмету є обов'язковою."
            else:
                data['subject'] = subject

            examdate = request.POST.get('examdate', '').strip()
            if not examdate:
                errors['examdate'] = u"Дата іспиту є обов'язковою."
            else:
                try:
                    datetime.strptime(examdate, '%Y-%m-%d %H:%M')
                except Exception:
                    errors['examdate'] = u"Некоректний формат дати"
                else:
                    data['examdate'] = examdate

            teacher = request.POST.get('teacher', '').strip()
            if not teacher:
                errors['teacher'] = u"Інформація про викладача є обов'язковою."
            else:
                data['teacher'] = teacher

            exam_group = request.POST.get('exam_group', '').strip()
            if not exam_group:
                errors['exam_group'] = u"Група є обов'язковою."
            else:
                data['exam_group'] = Group.objects.get(pk=exam_group)

            if errors:
                messages.error(request, u"Виправте наступні помилки:")
                return render(request, 'students/exams_add.html', {'groups': groups, 'errors': errors})
            else:
                exam = Exam(**data)
                exam.save()
                messages.success(request, u"Іспит успішно додано.")
                return HttpResponseRedirect(reverse("exams"))
        else:
            messages.warning(request, u"Додавання групи скасовано")
            return HttpResponseRedirect(reverse("exams"))
    else:
        return render(request, 'students/exams_add.html', {'groups': groups})

def exam_edit(request, pk):
    groups = Group.objects.all()
    data = {}
    errors = {}
    exams = Exam.objects.filter(pk=pk)
    if len(exams) != 1:
        messages.error(request, u"Такого студента не знайдено")
        return HttpResponseRedirect(reverse("exams"))
    elif request.method == "POST":
        if request.POST.get('save_button') is not None:
            subject = request.POST.get('subject', '').strip()
            if not subject:
                errors['subject'] = u"Назва предмету є обов'язковою."
            else:
                data['subject'] = subject

            examdate = request.POST.get('examdate', '').strip()
            if not examdate:
                errors['examdate'] = u"Дата іспиту є обов'язковою."
            else:
                try:
                    datetime.strptime(examdate, '%Y-%m-%d %H:%M')
                except Exception:
                    errors['examdate'] = u"Некоректний формат дати"
                else:
                    data['examdate'] = examdate+":00"

            teacher = request.POST.get('teacher', '').strip()
            if not teacher:
                errors['teacher'] = u"Інформація про викладача є обов'язковою."
            else:
                data['teacher'] = teacher

            exam_group = request.POST.get('exam_group', '').strip()
            if not exam_group:
                errors['exam_group'] = u"Група є обов'язковою."
            else:
                data['exam_group'] = Group.objects.get(pk=exam_group)

            if errors:
                messages.error(request, u"Виправте наступні помилки:")
                return render(request, 'students/exams_edit.html', {'groups': groups, 'errors': errors, 'exam': exams[0]})
            else:
                exam = exams[0]
                exam.subject = data['subject']
                exam.examdate = data['examdate']
                exam.teacher = data['teacher']
                exam.exam_group = data['exam_group']
                exam.save()
                messages.success(request, u"Іспит успішно збережено.")
                return HttpResponseRedirect(reverse("exams"))
        else:
            messages.warning(request, u"Редагування групи скасовано")
            return HttpResponseRedirect(reverse("exams"))
    else:
        return render(request, 'students/exams_edit.html', {'groups': groups, 'exam': exams[0]})

def exams_delete(request, pk):
    exams = Exam.objects.filter(pk=pk)
    if len(exams) != 1:
        messages.error(request, u"Іспит не знайдено.")
        return HttpResponseRedirect(reverse("exams"))
    elif request.method == "POST":
        if request.POST.get('confirm_button') is not None:
            exams.delete()
            messages.success(request, u"Інформацію про іспит видалено.")
            return HttpResponseRedirect(reverse("exams"))
        else:
            messages.warning(request, u"Видалення іспиту скасовано.")
            return HttpResponseRedirect(reverse("exams"))
    else:
        return render(request, 'students/exams_delete.html', {'exam': exams[0]})
