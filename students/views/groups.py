# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models.groups import Group

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
        fields = '__all__'

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

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete group %s</h1>' % gid)
