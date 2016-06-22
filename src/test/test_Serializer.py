# coding: utf-8
from __future__ import unicode_literals
import json

from unittest import TestCase
import datetime
from django.db import models
from django.conf import settings
from dss.TimeFormatFactory import TimeFormatFactory
from dss.Serializer import serializer

__author__ = 'RaPoSpectre'


class Test_Serializer(TestCase):
    def setUp(self):
        self.time_func = TimeFormatFactory.get_time_func('string')
        # DATABASES = {
        #     'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': ':memory:',
        #     'USER': '',                      # Not used with sqlite3.
        #     'PASSWORD': '',                  # Not used with sqlite3.
        #     'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        #     'PORT': '',
        #     }
        # }
        # settings.configure(DATABASES=DATABASES, DEBUG=True)
        # class TestAuthor(models.Model):
        #     name = models.CharField(default='test_author')
        #
        #     def __unicode__(self):
        #         return self.name
        #
        # class TestTags(models.Model):
        #     tag = models.CharField(default='test_tag')
        #     create_time = models.DateTimeField(auto_now=True)
        #
        # class TestArticle(models.Model):
        #     title = models.CharField(default='test')
        #     content = models.CharField(default='test')
        #     author = models.ForeignKey(TestAuthor, related_name='author_art')
        #     tags = models.ManyToManyField(TestTags, related_name='tag_art')
        #     create_time = models.DateTimeField(auto_now=True)
        #
        #
        # self.author = TestAuthor()
        # self.author.save()
        # tags = TestTags(tag='tag1')
        # tags.save()
        # self.article = TestArticle(author=self.author)
        # self.article.tags.add(tags)
        # self.article.save()

    def test_serializer(self):
        test_data = {'title': 'test',
                     'name': 'attr',
                     'time': datetime.datetime(2015, 10, 10, 12),
                     'list': [{'content': 'list_content',
                               'time': datetime.datetime(2015, 10, 11, 9)},
                              {'content': 'list_content1',
                               'time': datetime.datetime(2015, 12, 22, 9)}]}
        result = serializer(test_data, datetime_format='string', output_type='raw')
        self.assertEqual(result['time'], '2015-10-10 12:00:00')
        self.assertIsInstance(result, dict)
        self.assertEqual(result['list'][0]['time'], '2015-10-11 09:00:00')
        result = serializer(test_data, datetime_format='timestamp', output_type='json')
        self.assertEqual(json.loads(result)['title'], 'test')
        self.assertEqual(json.loads(result)['list'][0]['content'], 'list_content')
