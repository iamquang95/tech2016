# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-02 12:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('a2ausers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('question', 'question'), ('answer', 'answer')], default='question', max_length=200)),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('total_vote', models.IntegerField(default=0)),
                ('num_comments', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_created', to='a2ausers.A2AUser')),
                ('followed_by', models.ManyToManyField(blank=True, related_name='followed_questions', to='a2ausers.A2AUser')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_posts', to='posts.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='a2ausers.A2AUser')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='votes',
            field=models.ManyToManyField(through='posts.Vote', to='a2ausers.A2AUser'),
        ),
    ]
