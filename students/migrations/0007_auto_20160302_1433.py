# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-02 14:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_exam'),
    ]

    operations = [
        migrations.CreateModel(
            name='Examresult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(max_length=256, verbose_name='\u041e\u0446\u0456\u043d\u043a\u0430')),
            ],
            options={
                'verbose_name': '\u041e\u0446\u0456\u043d\u043a\u0430',
                'verbose_name_plural': '\u041e\u0446\u0456\u043d\u043a\u0438',
            },
        ),
        migrations.AlterField(
            model_name='exam',
            name='teacher',
            field=models.CharField(max_length=256, verbose_name='\u0412\u0438\u043a\u043b\u0430\u0434\u0430\u0447'),
        ),
        migrations.AddField(
            model_name='examresult',
            name='result_exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Exam', verbose_name='\u0406\u0441\u043f\u0438\u0442'),
        ),
        migrations.AddField(
            model_name='examresult',
            name='result_student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Student', verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442'),
        ),
    ]