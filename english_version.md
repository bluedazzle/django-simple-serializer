# Django Simple Serializer

---

Django Simple Serializer is a serializer to help user serialize django data or python list into json\xml\dict data in a simple way.

## Why Django Simple Serializer ?


### django.core.serializers
 This is a django built-in serializers, it serialzie querset but not a single model object. In addition, if you have DateTimeField into your model, the serializers will not work well(if you'd like using serialized data directly)
### QuerySet.values()
 As above, QuerySet.values() also not work well if you have DateTimeField into your model.
### django-rest-framework serializers
 django-rest-framework is a powerful tools to help you build REST API quickly. It has a powerful serializer but you have to use it with create the corresponding model serializer object first. 
### django simple serializer
For some people, we just want to get serialized data quickly and simply, so i make a simple way to get serialized data without extra opertion, this is why django simple serializer.

## Requirements

### Python 2:

Django >= 1.5

Python >= 2.6

### Python 3:

Django >= 1.8

Python >= 3

## Installation

Install using pip:

    pip install django-simple-serializer

## Working with django simple serializer
### Serializing objects
Assuming that we have django models like these:

    class Classification(models.Model):
        c_name = models.CharField(max_length=30, unique=True)
    
    class Article(models.Model):
        caption = models.CharField(max_length=50)
        classification = models.ForeignKey(Classification, related_name='cls_art')
        content = models.TextField()
        publish = models.BooleanField(default=False)

a simple example with using django models above:

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list)

data:

    [{'read_count': 0, 'create_time': 1432392456.0, 'modify_time': 1432392456.0, 'sub_caption': u'first', 'comment_count': 0, u'id': 31}, {'read_count': 0, 'create_time': 1432392499.0, 'modify_time': 1432392499.0, 'sub_caption': u'second', 'comment_count': 0, u'id': 32}]

By default, the serializer return a list or a dict(for a single object), you can set the parameter “output_type” to decide the serializer return json/xml/list.

## API Guide

#### dss.Serializer
Provides the serializer

*function* serializer(*data, datetime_format='timestamp', output_type='dict', include_attr=None, exclude_attr=None, deep=False*)

#### Parameters:

* data(_Required_|(QuerySet, Page, list, django model object))-data to be processed
* datetime_format(_Optional_|string)-convert datetime into string.default "timestamp"
* output_type(_Optional_|string)-serialize type. default "dict"
* include_attr(_Optional_|(list, tuple))-only serialize attributes in include_attr list. default None
* exclude_attr(_Optional_|(list, tuple))-exclude attributes in exclude_attr list. default None
* foreign(_Optional_|bool)-determines if serializer serialize ForeignKeyField. default False
* many(_Optional_|bool)-determines if serializer serialize ManyToManyField. default False

#### Usage:

**datetime_format:**  

|parameters|intro|
| --------------  | :---: |
|string|convert datetime into string like "2015-05-10 10:19:22"|
|timestamp|convert datetime into timestamp like "1432124420.0"|  

example:

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list, datetime_format='string', output_type='json')

data:

    [
        {
            "read_count": 0,
            "sub_caption": "first",
            "publish": true,
            "content": "first article",
            "caption": "first",
            "comment_count": 0,
            "create_time": "2015-05-23 22:47:36",
            "modify_time": "2015-05-23 22:47:36",
            "id": 31
        },
        {
            "read_count": 0,
            "sub_caption": "second",
            "publish": false,
            "content": "second article",
            "caption": "second",
            "comment_count": 0,
            "create_time": "2015-05-23 22:48:19",
            "modify_time": "2015-05-23 22:48:19",
            "id": 32
        }
    ]

**output_type**  

|parameters|intro|
| --------------  | :---: |
|dict|convert data into dict or list|
|json|convert data into json|
|xml|convert data into xml|  

example:

    from dss.Serializer import serializer
    article_list = Article.objects.all()[0]
    data = serializer(article_list, output_type='xml')

data:  

    <?xml version="1.0" encoding="utf-8"?>
    <root>
        <read_count>0</read_count>
        <sub_caption>first</sub_caption>
        <publish>True</publish>
        <content>first article</content>
        <caption>first</caption>
        <comment_count>0</comment_count>
        <create_time>1432392456.0</create_time>
        <modify_time>1432392456.0</modify_time>
        <id>31</id>
    </root>  

**include_attr**

example:

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list, output_type='json', include_attr=('content', 'caption',))

data:  

    [
        {
            "content": "first article",
            "caption": "first"
        },
        {
            "content": "second article",
            "caption": "second"
        }
    ]

**exclude_attr**

example:

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list, output_type='json', exclude_attr=('content',))

data:  

        [
            {
                "read_count": 0,
                "sub_caption": "first",
                "publish": true,
                "caption": "first",
                "comment_count": 0,
                "create_time": 1432392456,
                "modify_time": 1432392456,
                "id": 31
            },
            {
                "read_count": 0,
                "sub_caption": "second",
                "publish": false,
                "caption": "second",
                "comment_count": 0,
                "create_time": 1432392499,
                "modify_time": 1432392499,
                "id": 32
            }
        ]
        
**foreign**

Serialize ForeignKeyField and its sub item

example:

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list, output_type='json', include_attr=('classification', 'caption', 'create_time', foreign=True)

data:  

        [
            {
                "caption": "first",
                "create_time": 1432392456,
                "classification": {
                    "create_time": 1429708506,
                    "c_name": "python",
                    "id": 1,
                    "modify_time": 1429708506
                }
            },
            {
                "caption": "second",
                "create_time": 1432392499,
                "classification": {
                    "create_time": 1430045890,
                    "c_name": "test",
                    "id": 5,
                    "modify_time": 1430045890
                }
            }
        ]

**many**
Serialize ManyToManyField

example:

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list, output_type='json', include_attr=('classification', 'caption', 'create_time', many=True)

No test data have ManyToManyField ，data format same as above

#### dss.Mixin
Serialize Mixin

    class JsonResponseMixin(object)
        datetime_type = 'string'                # Output datetime format. Default is “string”，other parameters see dss.Serializer.serializer
        foreign = False                         # If serialize ForeignField。Default is False
        many = False                            # If serialize ManyToManyField。Default is False
        include_attr = None                     # Only serialize the  attrs which in include_attr list。Default is None, accept a tuple contains attrs
        exclude_attr = None                     # serialize exclude attrs in exclude_attr list。Default is None, accept a tuple contains attrs

#### Statement:

Converts class based view into return json class based view，uses for DetailView and so on.

#### Usage:

example:

    # view.py
    from dss.Mixin import JsonResponseMixin
    from django.views.generic import DetailView
    from model import Article
    
    class TestView(JsonResponseMixin, DetailView):
        model = Article
        datetime_type = 'string'
        pk_url_kwarg = 'id'
    
    
    # urls.py
    from view import TestView
    urlpatterns = patterns('',
        url(r'^test/(?P<id>(\d)+)/$', TestView.as_view()),
    )
        
access：`localhost:8000/test/1/`

response:

    {
        "article": {
            "classification_id": 5, 
            "read_count": 0, 
            "sub_caption": "second", 
            "comments": [], 
            "content": "asdfasdfasdf", 
            "caption": "second", 
            "comment_count": 0, 
            "id": 32, 
            "publish": false
        }, 
        "object": {
            "classification_id": 5, 
            "read_count": 0, 
            "sub_caption": "second", 
            "comments": [], 
            "content": "asdfasdfasdf", 
            "caption": "second", 
            "comment_count": 0, 
            "id": 32, 
            "publish": false
        }, 
        "view": ""
    }


*class MultipleJsonResponseMixin(JsonResponseMixin):*

#### Statement:

Mixin for ListView to converts it return data into json/xml.

#### Usage:

example:

    # view.py
    from dss.Mixin import MultipleJsonResponseMixin
    from django.views.generic import ListView
    from model import Article
    
    class TestView(MultipleJsonResponseMixin, ListView):
        model = Article
        query_set = Article.objects.all()
        paginate_by = 1
        datetime_type = 'string'
    
    
    # urls.py
    from view import TestView
    urlpatterns = patterns('',
        url(r'^test/$', TestView.as_view()),
    )
        
access：`localhost:8000/test/`

response:

    {
        "paginator": "", 
        "article_list": [
            {
                "classification_id": 1, 
                "read_count": 2, 
                "sub_caption": "first", 
                "content": "first article", 
                "caption": "first", 
                "comment_count": 0, 
                "publish": false, 
                "id": 31
            }, 
            {
                "classification_id": 5, 
                "read_count": 0, 
                "sub_caption": "", 
                "content": "testseteset", 
                "caption": "hehe", 
                "comment_count": 0, 
                "publish": false, 
                "id": 33
            }, 
            {
                "classification_id": 5, 
                "read_count": 0, 
                "sub_caption": "second", 
                "content": "asdfasdfasdf", 
                "caption": "second", 
                "comment_count": 0, 
                "publish": false, 
                "id": 32
            }
        ], 
        "object_list": [
            {
                "classification_id": 1, 
                "read_count": 2, 
                "sub_caption": "first", 
                "content": "first article", 
                "caption": "first", 
                "comment_count": 0, 
                "publish": false, 
                "id": 31
            }, 
            {
                "classification_id": 5, 
                "read_count": 0, 
                "sub_caption": "", 
                "content": "testseteset", 
                "caption": "hehe", 
                "comment_count": 0, 
                "publish": false, 
                "id": 33
            }, 
            {
                "classification_id": 5, 
                "read_count": 0, 
                "sub_caption": "second", 
                "content": "asdfasdfasdf", 
                "caption": "second", 
                "comment_count": 0, 
                "publish": false, 
                "id": 32
            }
        ], 
        "page_obj": {
            "current": 1, 
            "next": 2, 
            "total": 3, 
            "page_range": [
                {
                    "page": 1
                }, 
                {
                    "page": 2
                }, 
                {
                    "page": 3
                }
            ], 
            "previous": null
        }, 
        "is_paginated": true, 
        "view": ""
    }

*class FormJsonResponseMixin(JsonResponseMixin):*

#### Statement:

Converts class based view into a return json data class based view，use for CreateView、UpdateView、FormView and so on.

#### Usage:

example:

    # view.py
    from dss.Mixin import FormJsonResponseMixin
    from django.views.generic import UpdateView
    from model import Article
    
    class TestView(FormJsonResponseMixin, UpdateView):
        model = Article
        datetime_type = 'string'
        pk_url_kwarg = 'id'
    
    
    # urls.py
    from view import TestView
    urlpatterns = patterns('',
        url(r'^test/(?P<id>(\d)+)/$', TestView.as_view()),
    )
        
access：`localhost:8000/test/1/`

response:

    {
        "article": {
            "classification_id": 5, 
            "read_count": 0, 
            "sub_caption": "second", 
            "content": "asdfasdfasdf", 
            "caption": "second", 
            "comment_count": 0, 
            "id": 32, 
            "publish": false
        }, 
        "form": [
            {
                "field": "caption"
            }, 
            {
                "field": "sub_caption"
            }, 
            {
                "field": "read_count"
            }, 
            {
                "field": "comment_count"
            }, 
            {
                "field": "classification"
            }, 
            {
                "field": "content"
            }, 
            {
                "field": "publish"
            }
        ], 
        "object": {
            "classification_id": 5, 
            "read_count": 0, 
            "sub_caption": "second", 
            "content": "asdfasdfasdf", 
            "caption": "second", 
            "comment_count": 0, 
            "id": 32, 
            "publish": false
        }, 
        "view": ""
    }
## 2.0.0 New Feature:
Add serialize extra data:

When we want to add extra data in model and serialize it, we can do like this:

```python
    def add_extra(article):
        comments = Comment.objects.filter(article=article)
        setattr(article, 'comments', comments)
    
    articles = Article.objects.all()
    map(add_extra, articles)
    result = serializer(articles)
```

The result will in "comments".

The extra data can be a normal data type data, an other Django model, dict, list even a QuerySet.


## History

### Current Version：2.0.6

##### 2017.03.22 v2.0.6:

Add support for Python 3

##### 2017.02.25 v2.0.5:

Add support for Django model trough attribute

##### 2016.10.27 v2.0.4:

Fix issue #2.
 
##### 2016.10.19 v2.0.3:
Optimize code.

Fix known bugs.

Fix issue #1

##### 2016.6.22 v2.0.2:

Fix when dev in cbv, if include_attr is not None, MultipleJsonResponseMixin will filter all data.

Fix datetime.datetime and datetime.time was formated as datetime.date  

Optimize code.

##### 2016.6.14 v2.0.1:

fix known bugs.

##### 2016.6.13 v2.0.0:

Rewrite serializer, optimizes serialize time. 

Fix known bugs. 

Add serialize support for all Django Field. 

New feature: add serialize extra data in model.

##### 2015.10.15 v1.0.0:
Refactoring code. 

add cbv json minxin class. 

add serialize support for ManyToManyField.

##### 2015.10.12: v0.0.2:

Fix bugs.

##### 2015.5.23: v0.0.1:

First version.

# License

Copyright © RaPoSpectre.

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.