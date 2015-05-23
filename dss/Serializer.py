import ujson
import xmltodict
import datetime
import copy

from TimeFormatFactory import TimeFormatFactory

try:
    from django.db import models
    from django.core.paginator import Page
    from django.db.models.query import QuerySet
except ImportError:
    raise RuntimeError('django is required in django simple serializer')


def serializer(data, datetime_format='timestamp', output_type='dict', include_attr=None, except_attr=None, deep=False):
    if data is None:
        return None
    result = []
    time_func = TimeFormatFactory.get_time_func(datetime_format)
    if isinstance(data, models.Model):
        data = [data]
    if isinstance(data, (QuerySet, list, Page)):
        for itm in data:
            attr_list = get_attr(itm, deep, time_func)
            if include_attr is not None:
                new_attr_list = {}
                for i in include_attr:
                    try:
                        new_attr_list[i] = attr_list[i]
                    except:
                        continue
                attr_list = new_attr_list
            if except_attr is not None:
                for i in except_attr:
                    try:
                        attr_list.pop(i)
                    except:
                        continue
            if isinstance(data, list):
                result = attr_list
                break
            else:
                result.append(copy.copy(attr_list))
    if output_type == 'json':
        return ujson.dumps(result)
    elif output_type == 'dict':
        return result
    elif output_type == 'xml':
        dd = {'root': result}
        return xmltodict.unparse(dd)
    return None

def get_attr(model_data, deep, time_func):
    attr_list = [f.name for f in model_data._meta.fields]
    dic_list = {}
    for itm in attr_list:
        if isinstance(getattr(model_data, itm), models.Model):
            if deep:
                dic_list[itm] = get_attr(getattr(model_data, itm), deep, time_func)
        elif isinstance(getattr(model_data, itm), datetime.datetime):
            dic_list[itm] = time_func(getattr(model_data, itm))
        else:
            dic_list[itm] = getattr(model_data, itm)
    if '_state' in dic_list:
            dic_list.pop('_state')
    return dic_list