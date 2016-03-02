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
from students.views import students, groups, journal, exams, examresults
from .settings import MEDIA_URL, MEDIA_ROOT, DEBUG
from django.conf.urls.static import static

urlpatterns = [
    # students urls
    url(r'^$', students.students_list, name='home'),
    url(r'^students/add/$',
        students.students_add,
        name='students_add'),
    url(r'^students/(?P<sid>\d+)/edit/$',
        students.students_edit,
        name='students_edit'),
    url(r'^students/(?P<sid>\d+)/delete/$',
        students.students_delete,
        name='students_delete'),

    # groups urls
    url(r'^groups$', groups.groups_list, name='groups'),
    url(r'^groups/add/$',
        groups.groups_add,
        name='groups_add'),
    url(r'^groups/(?P<gid>\d+)/edit/$',
        groups.groups_edit,
        name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete/$',
        groups.groups_delete,
        name='groups_delete'),

    # exams urls
    url(r'^exams$', exams.exams_list, name='exams'),
    url(r'^exams/add/$',
        exams.exams_add,
        name='exams_add'),
    url(r'^exams/(?P<eid>\d+)/edit/$',
        exams.exams_edit,
        name='exams_edit'),
    url(r'^exams/(?P<eid>\d+)/delete/$',
        exams.exams_delete,
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
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
