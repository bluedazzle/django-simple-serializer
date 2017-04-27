# Django Simple Serializer

---

[English Doc][1]

Django Simple Serializer 是一个可以帮助开发者快速将 Django 数据或者 python data 序列化为 json|raw 数据。

## 为什么要用 Django Simple Serializer ?

对于序列化 Django 数据的解决方案已经有以下几种：  

### django.core.serializers
 Django内建序列化器, 它可以序列化Django model query set 但无法直接序列化单独的Django model数据。如果你的model里含有混合数据 , 这个序列化器同样无法使用(如果你想直接使用序列化数据). 除此之外, 如果你想直接把序列化数据返回给用户,显然它包含了很多敏感及对用户无用对信息。
### QuerySet.values()
 和上面一样, QuerySet.values() 同样没法工作如果你的model里有 DateTimeField 或者其他特殊的 Field 以及额外数据。
### django-rest-framework serializers
 django-rest-framework 是一个可以帮助你快速构建 REST API 的强力框架。 他拥有完善的序列化器，但在使用之前你需要花费一些时间入门, 并学习 cbv 的开发方式, 对于有时间需求的项目显然这不是最好的解决方案。
### django simple serializer
我希望可以快速简单的序列化数据, 所以我设计了一种可以不用任何额外的配置与学习而将Django data 或者 python data 序列化为相应的数据的简单的方式。 这就是为什么我写了 django simple serializer。

django simple serializer 的实际例子: [我的个人网站后台数据接口](https://github.com/bluedazzle/django-vue.js-blog/blob/master/api/views.py "22") 

----------

## 运行需求

### Python 2:

Django >= 1.5

Python >= 2.6

### Python 3:

Django >= 1.8

Python >= 3

## 安装

Install using pip:

    pip install django-simple-serializer

## 使用 django simple serializer 进行开发
### 序列化Django data
假设我们有以下Django models：

    class Classification(models.Model):
        c_name = models.CharField(max_length=30, unique=True)
    
    class Article(models.Model):
        caption = models.CharField(max_length=50)
        classification = models.ForeignKey(Classification, related_name='cls_art')
        content = models.TextField()
        publish = models.BooleanField(default=False)

使用django simple serializer的简单例子：

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list)

data:

    [{'read_count': 0, 'create_time': 1432392456.0, 'modify_time': 1432392456.0, 'sub_caption': u'first', 'comment_count': 0, u'id': 31}, {'read_count': 0, 'create_time': 1432392499.0, 'modify_time': 1432392499.0, 'sub_caption': u'second', 'comment_count': 0, u'id': 32}]

默认情况下, 序列器会返回一个 list 或者 dict(对于单个model实例), 你可以设置参数 “output_type” 来决定序列器返回 json/raw.

----------

## API 手册

#### dss.Serializer
提供序列器

*function* serializer(*data, datetime_format='timestamp', output_type='raw', include_attr=None, exclude_attr=None, foreign=False, many=False, through=True*)

#### Parameters:

* data(_Required_|(QuerySet, Page, list, django model object))-待处理数据
* datetime_format(_Optional_|string)-如果包含 datetime 将 datetime 转换成相应格式.默认为 "timestamp"（时间戳）
* output_type(_Optional_|string)-serialize type. 默认“raw”原始数据，即返回list或dict
* include_attr(_Optional_|(list, tuple))-只序列化 include_attr 列表里的字段。默认为 None
* exclude_attr(_Optional_|(list, tuple))-不序列化 exclude_attr 列表里的字段。默认为 None
* foreign(_Optional_|bool)-是否序列化 ForeignKeyField 。include_attr 与 exclude_attr 对   ForeignKeyField 依旧有效。 默认为 False
* many(_Optional_|bool)-是否序列化 ManyToManyField 。include_attr 与 exclude_attr 对 ManyToManyField 依旧有效 默认为 False
* through(_Optional_|bool)-是否序列化 ManyToManyField 中 through 属性数据 默认为 True

#### 用法:

**datetime_format:**  

|parameters|intro|
| --------------  | :---: |
|string|转换 datetime 为字符串。如： "2015-05-10 10:19:22"|
|timestamp|转换 datetime 为时间戳。如： "1432124420.0"|  

例子:

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
|raw|将list或dict中的特殊对象序列化后输出为list或dict|
|dict|同 raw|  
|json|转换数据为 json|

~~xml 转换数据为 xml~~  (暂时去除)

例子:

    from dss.Serializer import serializer
    article_list = Article.objects.all()[0]
    data = serializer(article_list, output_type='json')

data:  

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
        }

**include_attr**

例子:

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

例子:

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

序列化数据中的 ForeignKeyField 及其子项目

例子:

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
序列化 ManyToManyField

example:

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list, output_type='json', include_attr=('classification', 'caption', 'create_time', many=True)

测试数据无 ManyToManyField ，数据格式同上

#### dss.Mixin
提供序列器 Mixin

    class JsonResponseMixin(object)
        datetime_type = 'string'                # 输出datetime时间格式。默认为“string”，可选参数相见dss.Serializer.serializer
        foreign = False                         # 是否序列化ForeignField。默认为False
        many = False                            # 是否序列化ManyToManyField。默认为False
        include_attr = None                     # 只序列化include_attr包含的属性。默认为None,接受一个包含属性名称的tuple
        exclude_attr = None                     # 不序列化exclude_attr包含的属性。默认为None,接受一个包含属性名称的tuple
        through = True                          # 序列化 through 属性数据

#### 说明:

将普通class based view 转换为返回json数据的class based view，适用于DetailView等

#### 用法:

例子:

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
        
访问：`localhost:8000/test/1/`

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

#### 说明:

将列表类视图转换为返回json数据的类视图，适用于ListView等

#### 用法:

例子:

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
        
访问：`localhost:8000/test/`

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

#### 说明:

将普通class based view 转换为返回json数据的class based view，适用于CreateView、UpdateView、FormView等

#### 用法:

例子:

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
        
访问：`localhost:8000/test/1/`

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
## 2.0.0 新特点:
增加对额外数据的序列化支持:

当我们想在 model 中加入一些额外的数据并也想被序列化时, 现在可以这样做:

```python
    def add_extra(article):
        comments = Comment.objects.filter(article=article)
        setattr(article, 'comments', comments)
    
    articles = Article.objects.all()
    map(add_extra, articles)
    result = serializer(articles)
```

序列化的结果数据中将会包含"comments"哦.

额外加入的数据可以是一个普通的数据类型、 另一个 Django model、 字典、 列表甚至 QuerySet


## 版本历史

### 当前版本：2.0.7

##### 2017.04.26 v2.0.7:

修复 FileField、ImageFdFile 序列化问题

##### 2017.03.22 v2.0.6:

增加对 Python 3 的支持

##### 2017.02.25 v2.0.5:

增加对 trough 属性支持

##### 2016.10.27 v2.0.4:

修复 issue #2
 
##### 2016.10.19 v2.0.3:
优化代码

修复已知 bug

修复 issue #1

##### 2016.6.22 v2.0.2:

修复 cbv 下, 当有 include_attr 参数时, MultipleJsonResponseMixin 中所有数据被过滤的问题 

修复 datetime.datetime 和 datetime.time 都被格式化为 datetime.date 数据 

优化代码

##### 2016.6.14 v2.0.1:

修复发布 bug

##### 2016.6.13 v2.0.0:

重写 serializer, 优化序列化速度; 

修复已知 bug ; 

增加对所有 Django Field 的支持; 

新特性: 增加 model 额外数据的序列化支持

##### 2015.10.15 v1.0.0:
重构代码，修复bug； 

增加cbv json minxin 类 ； 

增加对ManyToManyField序列化支持。

##### 2015.10.12: v0.0.2:

bug修复。

##### 2015.5.23: v0.0.1:

第一版。

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

[1]: https://github.com/bluedazzle/django-simple-serializer/blob/master/english_version.md




