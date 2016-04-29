# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from models.students import Student
from models.groups import Group
from models.journal import JournalEntry
from models.exams import Exam
from models.examresults import Examresult


class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        """ Check if student is leader in any group
            If yes, then ensure it's the same as selected group. """

        # get group where current sudent is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(
                u"Студент є старостою іншої групи", code='invalid')

        return self.cleaned_data['student_group']


class GroupFormAdmin(ModelForm):

    def clean_leader(self):
        # print leader
        # print self.instance
        leader = self.cleaned_data['leader']
        if leader.student_group != self.instance:
            raise ValidationError(u"Студент навчається в іншій групі.", code='invalid')
        return self.cleaned_data['leader']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'card', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = [
        'last_name', 'first_name', 'middle_name', 'card', 'notes']
    form = StudentFormAdmin
    actions = ['copy']

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})

    def copy(self, request, queryset):
        for obj in queryset:
            obj.pk = None
            obj.save()
        if len(queryset) == 1:
            message = "Запис про студента"
        else:
            message = "Записи про студентів"
        self.message_user(request, "%s було успішно клоновані." % message)

    copy.short_description = "Клонувати виділені записи"


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    # list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_per_page = 10
    search_fields = ['title', 'leader__first_name', 'leader__last_name']
    form = GroupFormAdmin

    # def view_on_site(self, obj):
    #     return reverse('students_edit', kwargs={'pk': obj.id})


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(JournalEntry)
admin.site.register(Exam)
admin.site.register(Examresult)
