# coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
import json

from unittest import TestCase
from ..dss.Mixin import JsonResponseMixin, FormJsonResponseMixin, MultipleJsonResponseMixin

import datetime


class TestJsonResponseMixin(TestCase):
    def setUp(self):
        self.json_mixin = JsonResponseMixin()
        self.json_mixin.datetime_type = 'string'

    def test_time_format(self):
        res = self.json_mixin.time_format(datetime.datetime(2015, 12, 12, 12))
        self.assertEqual(res, '2015-12-12 12:00:00')

    def test_render_to_response(self):
        context = {'title': 'test', 'name': 'test_name'}
        resp = self.json_mixin.render_to_response(context=context)
        self.assertEqual(resp.content, json.dumps(context, indent=4))


class TestFormJsonResponseMixin(TestCase):
    def setUp(self):
        self.form_mixin = FormJsonResponseMixin()
        self.form_mixin.datetime_type = 'string'

        class TestForm(object):
            fields = ['form1', 'form2', 'form3']
        self.form = TestForm()

    def test_context_serialize(self):
        context = {'title': 'test_title',
                   'form': self.form}
        result = self.form_mixin.context_serialize(context)
        expect_res = {'title': 'test_title',
                      'form': [{'field': 'form1'},
                               {'field': 'form2'},
                               {'field': 'form3'}]}
        self.assertEqual(result, expect_res)


class TestMultipleJsonResponseMixin(TestCase):
    def setUp(self):
        self.multi_mixin = MultipleJsonResponseMixin()

        class TestPaginator(object):
            pass

        class TestPage(object):
            number = 1
            paginator = TestPaginator()
            setattr(paginator, 'num_pages', 3)
            setattr(paginator, 'page_range', [1, 2, 3])

            def previous_page_number(self):
                return None

            def next_page_number(self):
                return 2

        self.page_obj = TestPage()

    def test_context_serialize(self):
        context = {'page_obj': self.page_obj,
                   'is_paginated': True,
                   'title': 'test'}
        result = self.multi_mixin.context_serialize(context)
        expect_res = {'current': 1,
                      'total': 3,
                      'previous': None,
                      'next': 2,
                      'page_range': [{'page': 1},
                                     {'page': 2},
                                     {'page': 3}]}
        self.assertEqual(result['page_obj'], expect_res)