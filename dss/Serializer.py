#coding:utf-8
from __future__ import unicode_literals

import xmltodict
import datetime
import copy
import json

from TimeFormatFactory import TimeFormatFactory
from Warning import remove_check

try:
    from django.db import models
    from django.db.models import manager
    from django.core.paginator import Page
    from django.db.models.query import QuerySet
    import django
except ImportError:
    raise RuntimeError('django is required in django simple serializer')


def include_check(include_attr, attr_dict):
    if include_attr:
        ex_attr_dict = copy.deepcopy(attr_dict)
        attr_dict.clear()
        for attr in include_attr:
            attr_dict[attr] = ex_attr_dict.get(attr, None)
    return attr_dict


def exclude_check(exclude_attr, attr_dict):
    if exclude_attr:
        for attr in exclude_attr:
            if attr in attr_dict:
                attr_dict.pop(attr)
    return attr_dict


def get_attr(model_data, time_func, foreign, many):
    dic_list = {}
    attr_list = model_data._meta.get_all_field_names()
    for itm in attr_list:
        attribute = getattr(model_data, itm)
        if isinstance(attribute, models.Model):
            if foreign:
                dic_list[itm] = get_attr(attribute, time_func, foreign, many)
        elif isinstance(attribute, manager.Manager):
            if many and not str(itm).endswith('_art'):
                many_obj = attribute.all()
                many_list = []
                for mitm in many_obj:
                    many_item = get_attr(mitm, time_func, foreign, many)
                    many_list.append(many_item)
                dic_list[itm] = many_list
        elif isinstance(attribute, datetime.datetime):
            dic_list[itm] = time_func(getattr(model_data, itm))
        else:
            dic_list[itm] = getattr(model_data, itm)
    if '_state' in dic_list:
            dic_list.pop('_state')
    return dic_list


def data_convert(data, time_func, foreign, many, include_attr, exclude_attr):
    if isinstance(data, models.Model):
        attr_list = get_attr(data, time_func, foreign, many)
        include_check(include_attr, attr_list)
        exclude_check(exclude_attr, attr_list)
        return attr_list
    elif isinstance(data, (QuerySet, Page)):
        result = []
        for itm in data:
            attr_list = get_attr(itm, time_func, foreign, many)
            include_check(include_attr, attr_list)
            exclude_check(exclude_attr, attr_list)
            result.append(copy.copy(attr_list))
        return result
    elif isinstance(data, datetime.datetime):
        return time_func(data)
    else:
        return data


def output_convert(output_type, data):
    output_switch = {'dict': data,
                     'raw': data,
                     'json': json.dumps(data, indent=4),
                     'xml': xmltodict.unparse({'root': data})}
    return output_switch.get(output_type, None)


def serializer(data, datetime_format='timestamp', output_type='raw', include_attr=None, exclude_attr=None,
               foreign=False, many=False, **kwargs):
    foreign = remove_check(**kwargs) or foreign
    time_func = TimeFormatFactory.get_time_func(datetime_format)
    result = data_convert(data, time_func, foreign, many, include_attr, exclude_attr)
    return output_convert(output_type, result)