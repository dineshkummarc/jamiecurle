from django.contrib import admin

from django.contrib.contenttypes import generic
from models import Img, Css, Js

class ImgInline(generic.GenericTabularInline):
    model = Img

class CssInline(generic.GenericTabularInline):
    model = Css

class JsInline(generic.GenericTabularInline):
    model = Js

admin.site.register(Img)
admin.site.register(Js)
admin.site.register(Css)