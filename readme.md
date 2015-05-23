# Django Simple Serializer

---

Django Simple Serializer is a serializer to help user serialize django data or python list into json\xml\dict data in a simple way.

##Why Django Simple Serializer ?

---

###django.core.serializers
 This is a django built-in serializers, it serialzie querset but not a single model object. In addition, if you have DateTimeField into your model, the serializers will not work well(if you'd like using serialized data directly)
###QuerySet.values()
 As above, QuerySet.values() also not work well if you have DateTimeField into your model.
###django-rest-framework serializers
 django-rest-framework is a powerful tools to help you build REST API quickly. It has a powerful serializer but you have to use it with create the corresponding model serializer object first. 
###django simple serializer
For some people, we just want to get serialized data quickly and simply, so i make a simple way to get serialized data without extra opertion, this is why django simple serializer.

##Requirements

---

Django >= 1.4

##Installation

---

Install using pip:

    pip install django-simple-serializer

##Working with django simple serializer

---

#License