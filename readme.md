# Django Simple Serializer

---

Django Simple Serializer is a serializer to help user serialize django data or python list into json\xml\dict data in a simple way.

##Why Django Simple Serializer ?


###django.core.serializers
 This is a django built-in serializers, it serialzie querset but not a single model object. In addition, if you have DateTimeField into your model, the serializers will not work well(if you'd like using serialized data directly)
###QuerySet.values()
 As above, QuerySet.values() also not work well if you have DateTimeField into your model.
###django-rest-framework serializers
 django-rest-framework is a powerful tools to help you build REST API quickly. It has a powerful serializer but you have to use it with create the corresponding model serializer object first. 
###django simple serializer
For some people, we just want to get serialized data quickly and simply, so i make a simple way to get serialized data without extra opertion, this is why django simple serializer.

##Requirements

Django >= 1.4
Python >= 2.6.0

##Installation

Install using pip:

    pip install django-simple-serializer

##Working with django simple serializer
###Serializing objects
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

##API Guide

####dss.Serializer
Provides the serializer

*function* serializer(*data, datetime_format='timestamp', output_type='dict', include_attr=None, except_attr=None, deep=False*)

####Parameters:

* data(_Required_|(QuerySet, Page, list, django model object))-data to be processed
* datetime_format(_Optional_|string)-convert datetime into string.default "timestamp"
* output_type(_Optional_|string)-serialize type. default "dict"
* include_attr(_Optional_|(list, tuple))-only serialize attributes in include_attr list. default None
* except_attr(_Optional_|(list, tuple))-exclude attributes in except_attr list. default None
* deep(_Optional_|bool)-determines if serializer serialize ForeignKeyField. default False

####Usage:  

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

**except_attr**

example:

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list, output_type='json', except_attr=('content',))

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
        
**deep**

example:

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list, output_type='json', include_attr=('classification', 'caption', 'create_time', deep=True)

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

#License

Copyright © Tom Christie.

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
