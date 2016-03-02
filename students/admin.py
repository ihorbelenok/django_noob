from django.contrib import admin
from models.students import Student
from models.groups import Group
from models.journal import JournalEntry
from models.exams import Exam
from models.examresults import Examresult

# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(JournalEntry)
admin.site.register(Exam)
admin.site.register(Examresult)
