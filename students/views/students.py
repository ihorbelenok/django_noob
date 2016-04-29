# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.students import Student
from ..models.groups import Group
from endless_pagination.decorators import page_template
from endless_pagination import utils
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib import messages

from PIL import Image

from django import forms
from django.forms import ModelForm, ValidationError
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from crispy_forms.bootstrap import FormActions


@page_template('students/students_page.html')
def students_list(request,
                  template='students/students_list.html',
                  page_template='students/students_page.html',
                  extra_context=None):
    if request.method == "POST":
        selected = request.POST.getlist('student_select')
        studlist = '/'.join(selected)
        studlist = studlist + "/"
        return HttpResponseRedirect(reverse("students_delete", kwargs={'studlist': studlist}))
    else:
        students = Student.objects.all().order_by('last_name')

        order_by = request.GET.get('order_by', '')
        if order_by in ('last_name', 'first_name', 'card', 'id'):
            students = students.order_by(order_by)
            if request.GET.get('reverse', '') == '1':
                students = students.reverse()

        context = {'students': students,
                   'page_template': page_template,
                   'start_id': (utils.get_page_number_from_request(request) - 1) * 10,
                   'per_page': 10}

        if extra_context is not None:
            context.update(extra_context)
        if request.is_ajax():
            template = page_template

        return render(request, template, context)


def students_add(request):
    if request.method == "POST":
        if request.POST.get('add_button') is not None:
            errors = {}

            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            # validating user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Імʼя є обовʼязковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обовʼязковим"
            else:
                data['last_name'] = last_name

            birth_date = request.POST.get('birth_date', '').strip()
            if not birth_date:
                errors['birth_date'] = u"Дата народження є обовʼязковою"
            else:
                try:
                    datetime.strptime(birth_date, '%Y-%m-%d')
                except Exception:
                    errors[
                        'birth_date'] = u"Введіть коректний формат дати (напр. 1987-12-30)"
                else:
                    data['birth_date'] = birth_date

            card = request.POST.get('card', '').strip()
            if not card:
                errors['card'] = u"Номер білета є обовʼязковим"
            else:
                data['card'] = card

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Група є обовʼязковою"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                if photo.name.split(".")[-1].lower() not in ('jpg', 'jpeg', 'png', 'gif'):
                    errors[
                        'photo'] = u"Файл має бути одного з наступних типів: jpg, jpeg, png, gif"
                else:
                    try:
                        Image.open(photo)
                    except Exception:
                        errors[
                            'photo'] = u"Завантажений файл не є файлом зображення або пошкоджений"
                    else:
                        if photo.size > 2 * 1024 * 1024:
                            errors[
                                'photo'] = u"Фото занадто велике (розмір файлу має бути менше 2Мб)"
                        else:
                            data['photo'] = photo

            if not errors:
                student = Student(**data)
                student.save()
                messages.success(
                    request, u'Студента "%s" успішно додано!' % student)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            messages.warning(request, u"Додавання студента скасовано!")
            return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'students/students_add.html',
                      {'groups': Group.objects.all().order_by('title')})


class StudentAddForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name',
                  'last_name',
                  'middle_name',
                  'birth_date',
                  'photo',
                  'card',
                  'student_group',
                  'notes']

    def __init__(self, *args, **kwargs):
        super(StudentAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_add')
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
            Button('cancel_button', u'Скасувати', onclick='window.location.href="{}"'.format(reverse('home'))))


class StudentAddView(CreateView):
    model = Student
    template_name = 'students/students_add_edit.html'
    form_class = StudentAddForm

    def get_success_url(self):
        messages.success(self.request, u"Студента успішно додано!")
        return reverse('home')

    # def post(self, request, *args, **kwargs):
    #     if request.POST.get('cancel_button'):
    #         messages.warning(request, u"Додавання студента відмінено!")
    #         return HttpResponseRedirect(reverse('home'))
    #     else:
    #         return super(StudentAddView, self).post(request, *args, **kwargs)


class StudentList(ListView):
    model = Student
    context_object_name = 'students'
    template = 'students/student_class_based_view_template'

    def get_context_data(self, **kwargs):
        """ This method adds extra variables to template"""
        # get original context data from parent class
        context = super(StudentList, self).get_context_data(**kwargs)

        # tell template not to show logo on a page
        context['show_logo'] = False

        # return context mapping
        return context

    def get_queryset(self):
        """ Order students by last_name"""
        # get original query set
        qs = super(StudentList, self).get_queryset()

        # order by last name
        return qs.order_by('last_name')


class StudentUpdateForm(ModelForm):

    class Meta:
        model = Student
        fields = ['first_name',
                  'last_name',
                  'middle_name',
                  'birth_date',
                  'photo',
                  'card',
                  'student_group',
                  'notes']

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse(
            'students_edit', kwargs={'pk': kwargs['instance'].id})
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
            Button('cancel_button', u'Скасувати', onclick='window.location.href="{}"'.format(reverse('home'))))

    def clean_student_group(self):
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(
                u"Студент є старостою іншої групи", code='invalid')

        return self.cleaned_data['student_group']


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_add_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        messages.success(self.request, u"Студента успішно збережено!")
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Редагування студента відмінено!")
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


def student_edit_manual(request, pk):
    students = Student.objects.filter(pk=pk)
    groups = Group.objects.all()

    if len(students) != 1:
        messages.error(request, 'Обраного студента не існує')
        return HttpResponseRedirect(reverse('home'))
    elif request.method == "POST":
        st = Student.objects.get(pk=pk)
        if request.POST.get('save_button') is not None:
            st.middle_name = request.POST.get('middle_name', '').strip()
            st.notes = request.POST.get('notes', '').strip()
            errors = {}

            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Імʼя є обовʼязковим."
            else:
                st.first_name = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обовʼязковим."
            else:
                st.last_name = last_name

            birth_date = request.POST.get('birth_date', '').strip()
            if not birth_date:
                errors['birth_date'] = u"Дата народження є обовʼязковою."
            else:
                try:
                    bd = datetime.strptime(birth_date, '%Y-%m-%d')
                except Exception:
                    errors['birth_date'] = u"Введіть коректний формат дати (напр. 1987-12-30)"
                else:
                    st.birth_date = bd

            if request.POST.get('photo-clear') is not None:
                st.photo = None
            else:
                photo = request.FILES.get('photo')
                if photo:
                    if photo.name.split(".")[-1].lower() not in ('jpg', 'jpeg', 'png', 'gif'):
                        errors[
                            'photo'] = u"Файл має бути одного з наступних типів: jpg, jpeg, png, gif"
                    else:
                        try:
                            Image.open(photo)
                        except Exception:
                            errors[
                                'photo'] = u"Завантажений файл не є файлом зображення або пошкоджений"
                        else:
                            if photo.size > 2 * 1024 * 1024:
                                errors[
                                    'photo'] = u"Фото занадто велике (розмір файлу має бути менше 2Мб)"
                            else:
                                st.photo = request.FILES.get('photo')

            card = request.POST.get('card', '').strip()
            if not card:
                errors['card'] = u"Номер білета є обовʼязковим."
            else:
                st.card = card

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Група є обовʼязковою"
            else:
                gr = Group.objects.filter(pk=student_group)
                if len(gr) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    grps = Group.objects.filter(leader=Student.objects.get(pk=pk))
                    if len(grps) > 0 and int(student_group) != grps[0].pk:
                        errors['student_group'] = u"Студент є старостою іншої групи"
                    else:
                        st.student_group = gr[0]

            if errors:
                messages.error(request, "Виправте, будь-ласка, наступні помилки:")
                return render(request, 'students/students_edit.html', {'pk': pk, 'student': st, 'errors': errors, 'groups': groups})
            else:
                st.save()
                messages.success(
                    request, 'Інформацію по студенту "%s" успішно збережено.' % students[0])
                return HttpResponseRedirect(reverse('home'))
        elif request.POST.get('cancel_button') is not None:
            messages.warning(request, 'Редагування студента скасовано.')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, 'Упс! Щось пішло не так. Повторіть спробу пізніше.')
            return HttpResponseRedirect(reverse('home'))
    else:
        return render(request,
                      'students/students_edit.html',
                      {'pk': pk, 'student': students[0], 'groups': groups})


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Студента успішно видалено!")
        return reverse('home')


def students_delete(request, studlist):
    selected = studlist[0:-1].split('/')
    selected = map(int, selected)
    students = Student.objects.filter(pk__in=selected)
    if (len(students) != len(selected)) or len(selected) == 0:
        messages.error(request, 'Одного або декількох з обраних студентів не існує.')
        return HttpResponseRedirect(reverse('home'))
    else:
        if request.method == "POST":
            if request.POST.get('confirm_button') is not None:
                name = ""
                for pk in selected:
                    student = Student.objects.get(pk=pk)
                    name = name + "'" + student.__str__() + "', "
                    student.delete()
                messages.success(request, "Успішно видалено: %s." % name[0:-2])
                return HttpResponseRedirect(reverse('home'))
            elif request.POST.get('cancel_button') is not None:
                messages.warning(request, "Видалення студентів скасовано.")
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, "Упс! Щось пішло не так. Повторіть спробу пізніше.")
                return HttpResponseRedirect(reverse('home'))
        else:
            return render(request,
                          'students/students_delete.html',
                          {'studlist': studlist, 'students': students})
