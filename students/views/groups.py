# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.groups import Group
from ..models.students import Student

from django.core.urlresolvers import reverse

from endless_pagination.decorators import page_template
from endless_pagination import utils

from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView, DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button

from django.contrib import messages


@page_template('students/groups_page.html')
def groups_list(request,
                template='students/groups.html',
                page_template='students/groups_page.html',
                extra_context=None):
    groups = Group.objects.all().order_by('title')
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'id'):
        groups = groups.order_by(order_by)
    elif order_by == 'leader':
        groups = groups.order_by("leader__first_name")
    if request.GET.get('reverse', '') == '1':
        groups = groups.reverse()

    context = {"groups": groups,
               'page_template': page_template,
               'start_id': (utils.get_page_number_from_request(request)-1)*15,
               'per_page': 15}

    if extra_context is not None:
        context.update(extra_context)
    if request.is_ajax():
        template = page_template

    return render(request,
                  template,
                  context)


class GroupAddForm(ModelForm):
    class Meta:
        model = Group
        fields = ('title', 'notes')

    def __init__(self, *args, **kwargs):
        super(GroupAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('groups_add')
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
            Button('cancel_button', u'Скасувати', onclick='window.location.href="{}"'.format(reverse('groups'))))

class GroupAddView(CreateView):
    model = Group
    template_name = 'students/groups_add_edit.html'
    form_class = GroupAddForm

    def get_success_url(self):
        messages.success(self.request, u"Групу успішно додано!")
        return reverse('groups')

class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)
        self.fields['leader'].queryset = Student.objects.filter(student_group=self.instance)
        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('groups_edit', kwargs={'pk': self.instance.id})
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
            Button('cancel_button', u'Скасувати', onclick='window.location.href="{}"'.format(reverse('groups'))))

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/groups_add_edit.html'
    form_class = GroupUpdateForm

    def get_success_url(self):
        messages.success(self.request, u"Групу успішно додано!")
        return reverse('groups')


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Групу успішно видалено!")
        return reverse('groups')


def group_add(request):
    data = {}
    if request.method == 'POST':
        if request.POST.get('add_button') is not None:
            errors = {}
            data['notes'] = request.POST.get('notes', '').strip()

            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = u"Назва є обов'язковою."
            else:
                groups = Group.objects.filter(title=title)
                if len(groups) > 0:
                    errors['title'] = u"Така група вже існує"
                else:
                    data['title'] = title

            if not errors:
                group = Group(**data)
                group.save()
                messages.success(request, u"Група успішно створена")
                return HttpResponseRedirect(reverse("groups"))
            else:
                messages.error(request, u"Виправте наступні помилки:")
                return render(request, 'students/groups_add.html', {'errors': errors})
        else:
            messages.warning(request, u"Додавання студента скасовано.")
            return HttpResponseRedirect(reverse("groups"))
    else:
        return render(request, 'students/groups_add.html', {})

def group_edit(request,pk):
    students = Student.objects.filter(student_group=pk)
    groups = Group.objects.filter(pk=pk)
    data = {}
    if len(groups) != 1:
        messages.error(request, u"Такої групи не існує.")
        return HttpResponseRedirect(reverse("groups"))
    else:
        if request.method == "POST":
            if request.POST.get('save_button') is not None:
                errors = {}
                data['notes'] = request.POST.get('notes', '').strip()

                title = request.POST.get('title', '').strip()
                if not title:
                    errors['title'] = u"Назва є обов'язковою."
                else:
                    data['title'] = title

                leader = request.POST.get('leader', '').strip()
                if not leader:
                    data['leader'] = leader
                else:
                    leader = int(leader)
                    if len(students.filter(pk=leader)) != 1:
                        errors['leader'] = u"Оберіть коректного старосту."
                    else:
                        data['leader'] = leader

                if not errors:
                    group = groups[0]
                    group.title = data['title']
                    if data['leader']:
                        group.leader = Student.objects.get(pk = data['leader'])
                    else:
                        group.leader = None
                    group.notes = data['notes']
                    group.save()
                    messages.success(request, u"Група успішно змінена")
                    return HttpResponseRedirect(reverse("groups"))
                else:
                    messages.error(request, u"Виправте наступні помилки:")
                    return render(request, 'students/groups_edit.html', {'errors': errors, 'students': students, 'group': groups[0], 'pk': pk})
            else:
                messages.warning(request, u"Редагування групи скасовано.")
                return HttpResponseRedirect(reverse("groups"))
        else:
            return render(request, 'students/groups_edit.html', {'students': students, 'group': groups[0], 'pk': pk})

def groups_delete(request, pk):
    group = Group.objects.get(pk=pk)
    if request.method == "POST":
        if request.POST.get('confirm_button') is not None:
            group.delete()
            messages.success(request, u"Інформацію про групу видалено.")
            return HttpResponseRedirect(reverse("groups"))
        else:
            messages.warning(request, u"Видалення групи скасовано.")
            return HttpResponseRedirect(reverse("groups"))
    else:
        return render(request, 'students/groups_delete.html', {'group': group, 'pk': pk})
