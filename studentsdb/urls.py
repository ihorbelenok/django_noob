"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from students.views import students, groups, journal, exams, examresults, contact_admin
from .settings import MEDIA_URL, MEDIA_ROOT, DEBUG
from django.conf.urls.static import static


urlpatterns = [
    # students urls
    url(r'^$', students.students_list, name='home'),
    url(r'^students/add/$',
        # students.students_add,            # fully handmade
        students.StudentAddView.as_view(),  # modelform+createview
        name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$',
        students.StudentUpdateView.as_view(), # modelform+updateview
        # students.student_edit_manual,           # fully handmade
        name='students_edit'),
    url(r'^students/(?P<studlist>(?:\d+/)+)delete/$',
        # students.StudentDeleteView.as_view(), # deleteview
        students.students_delete,                # fully handmade
        name='students_delete'),
    url(r'^students/(?P<pk>\d+)/delete/$',
        # students.StudentDeleteView.as_view(), # deleteview
        students.students_delete,                # fully handmade
        name='student_delete'),
    url(r'^student_list/$', students.StudentList.as_view()),

    # groups urls
    url(r'^groups$', groups.groups_list, name='groups'),
    url(r'^groups/add/$',
        # groups.GroupAddView.as_view(),      # addview
        groups.group_add,                    # handmade
        name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$',
        # groups.GroupUpdateView.as_view(),   # updateview
        groups.group_edit,                  # handmade
        name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$',
        # groups.GroupDeleteView.as_view(),   # deleteview
        groups.groups_delete,               # handmade
        name='groups_delete'),

    # exams urls
    url(r'^exams$', exams.exams_list, name='exams'),
    url(r'^exams/add/$',
        # exams.ExamAddView.as_view(),        #addview
        exams.exam_add,                     # handmade
        name='exams_add'),
    url(r'^exams/(?P<pk>\d+)/edit/$',
        # exams.ExamUpdateView.as_view(),     # updateview
        exams.exam_edit,                    # handmade
        name='exams_edit'),
    url(r'^exams/(?P<pk>\d+)/delete/$',
        # exams.ExamDeleteView.as_view(),     # deleteview
        exams.exams_delete,                 # handmade
        name='exams_delete'),

    # exam results urls
    url(r'^examresults$', examresults.examresults_list, name='examresults'),
    url(r'^examresults/add/$',
        examresults.examresults_add,
        name='examresults_add'),
    url(r'^examresults/(?P<rid>\d+)/edit/$',
        examresults.examresults_edit,
        name='examresults_edit'),
    url(r'^examresults/(?P<rid>\d+)/delete/$',
        examresults.examresults_delete,
        name='examresults_delete'),

    url(r'^journal$', journal.journal, name='journal'),

    url(r'^admin/', admin.site.urls),

    # contact admin form
    url(r'^contact-admin/$', contact_admin.ContactView.as_view(), name='contact_admin'),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
