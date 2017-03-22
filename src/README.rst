Django Simple Serializer
========================

--------------

[English Doc][1]

Django Simple Serializer 是一个可以帮助开发者快速将 Django 数据或者
python data 序列化为 json\|raw 数据。

为什么要用 Django Simple Serializer ?
-------------------------------------

对于序列化 Django 数据的解决方案已经有以下几种：

django.core.serializers
~~~~~~~~~~~~~~~~~~~~~~~

Django内建序列化器, 它可以序列化Django model query set
但无法直接序列化单独的Django model数据。如果你的model里含有混合数据 ,
这个序列化器同样无法使用(如果你想直接使用序列化数据). 除此之外,
如果你想直接把序列化数据返回给用户,显然它包含了很多敏感及对用户无用对信息。

QuerySet.values()
~~~~~~~~~~~~~~~~~

和上面一样, QuerySet.values() 同样没法工作如果你的model里有
DateTimeField 或者其他特殊的 Field 以及额外数据。

django-rest-framework serializers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

django-rest-framework 是一个可以帮助你快速构建 REST API 的强力框架。
他拥有完善的序列化器，但在使用之前你需要花费一些时间入门, 并学习 cbv
的开发方式, 对于有时间需求的项目显然这不是最好的解决方案。

django simple serializer
~~~~~~~~~~~~~~~~~~~~~~~~

我希望可以快速简单的序列化数据,
所以我设计了一种可以不用任何额外的配置与学习而将Django data 或者 python
data 序列化为相应的数据的简单的方式。 这就是为什么我写了 django simple
serializer。

django simple serializer 的实际例子: `我的个人网站后台数据接口`_

--------------

运行需求
--------

Python 2:
~~~~~~~~~

Django >= 1.5

Python >= 2.6

Python 3:
~~~~~~~~~

Django >= 1.8

Python >= 3

安装
----

Install using pip:

::

    pip install django-simple-serializer

使用 django simple serializer 进行开发
--------------------------------------

序列化Django data
~~~~~~~~~~~~~~~~~

假设我们有以下Django models：

::

    class Classification(models.Model):
        c_name = models.CharField(max_length=30, unique=True)

    class Article(models.Model):
        caption = models.CharField(max_length=50)
        classification = models.ForeignKey(Classification, related_name='cls_art')
        content = models.TextField()
        publish = models.BooleanField(default=False)

使用django simple serializer的简单例子：

::

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list)

data:

::

    [{'read_count': 0, 'create_time': 1432392456.0, 'modify_time': 1432392456.0, 'sub_caption': u'first', 'comment_count': 0, u'id': 31}, {'read_count': 0, 'create_time': 1432392499.0, 'modify_time': 1432392499.0, 'sub_caption': u'second', 'comment_count': 0, u'id': 32}]

默认情况下, 序列器会返回一个 list 或者 dict(对于单个model实例),
你可以设置参数 “output\_type” 来决定序列器返回 json/raw.

--------------

API 手册
--------

dss.Serializer
^^^^^^^^^^^^^^

提供序列器

*function* serializer(\ *data, datetime\_format=‘timestamp’,
output\_type=‘raw’, include\_attr=None, exclude\_attr=None,
foreign=False, many=False, through=True*)

Parameters:
^^^^^^^^^^^

-  data(\ *Required*\ \|(QuerySet, Page, list, django model
   object))-待处理数据
-  datetime\_format(\ *Optional*\ \|string)-如果包含 datetime 将
   datetime 转换成相应格式.默认为 “timestamp”（时间戳）
-  output\_type(\ *Optional*\ \|string)-serialize type.
   默认“raw”原始数据，即返回list或dict
-  include\_attr(\ *Optional*\ \|(list, tuple))-只序列化 include\_attr
   列表里的字段。默认为 None
-  exclude\_attr(\ *Optional*\ \|(list, tuple))-不序列化 exclude\_attr
   列表里的字段。默认为 None
-  foreign(\ *Optional*\ \|bool)-是否序列化 ForeignKeyField
   。include\_attr 与 exclude\_attr 对 ForeignKeyField 依旧有效。 默认为
   False
-  many(\ *Optional*\ \|bool)-是否序列化 ManyToManyField 。include\_attr
   与 exclude\_attr 对 ManyToManyField 依旧有效 默认为 False
-  through(\ *Optional*\ \|bool)-是否序列化 ManyToManyField 中 through
   属性数据 默认为 True

.. _我的个人网站后台数据接口: https://github.com/bluedazzle/django-vue.js-blog/blob/master/api/views.py
用法:
^^^^^

**datetime\_format:**

+--------------+------------------------------------------------------+
| parameters   | intro                                                |
+==============+======================================================+
| string       | 转换 datetime 为字符串。如： “2015-05-10 10:19:22”   |
+--------------+------------------------------------------------------+
| timestamp    | 转换 datetime 为时间戳。如： “1432124420.0”          |
+--------------+------------------------------------------------------+

例子:

::

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list, datetime_format='string', output_type='json')

data:

::

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

**output\_type**

+--------------+----------------------------------------------------+
| parameters   | intro                                              |
+==============+====================================================+
| raw          | 将list或dict中的特殊对象序列化后输出为list或dict   |
+--------------+----------------------------------------------------+
| dict         | 同 raw                                             |
+--------------+----------------------------------------------------+
| json         | 转换数据为 json                                    |
+--------------+----------------------------------------------------+

[STRIKEOUT:xml 转换数据为 xml] (暂时去除)

例子:

::

    from dss.Serializer import serializer
    article_list = Article.objects.all()[0]
    data = serializer(article_list, output_type='json')

data:

::

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

**include\_attr**

例子:

::

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list, output_type='json', include_attr=('content', 'caption',))

data:

::

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

**exclude\_attr**

例子:

::

    from dss.Serializer import serializer
    article_list = Article.objects.all()
    data = serializer(article_list, output_type='json', exclude_attr=('content',))

data:

::

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