from django.db import models
from south.modelsinspector import add_introspection_rules
from apps.utils.fields import ImageWithThumbsField
from django.conf import settings

# Create your models here.

class StyleSheet(models.Model):
    path = models.FilePathField(path="%s/templates/blog/css" % settings.APP_ROOT, recursive=True)
    
    def __unicode__(self):
        return u'%s' % self.path
    
    @property
    def template(self):
        return self.path.replace('%s/templates/' % settings.APP_ROOT, '')
    

class Script(models.Model):
    path = models.FilePathField(path="%s/templates/blog/js" % settings.APP_ROOT, recursive=True)
    
    def __unicode__(self):
        return u'%s' % self.path
    
    @property
    def template(self):
        return self.path.replace('%s/templates/' % settings.APP_ROOT, '')
    

class Post(models.Model):
    IMG_CACHE = False
    HIDDEN = 1
    DRAFT = 2
    PUBLISHED = 3
        
    STATUS_CHOICES  = (
        (HIDDEN, 'Hidden'),
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    stylesheets = models.ManyToManyField(StyleSheet, blank=True, null=True,)
    scripts = models.ManyToManyField(Script, blank=True, null=True)
    content = models.TextField()
    status = models.SmallIntegerField(default=DRAFT, choices=STATUS_CHOICES)
    featured = models.BooleanField(default=False)
    comments = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'%s' % self.pk
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog_post', (), {
            'year' : self.created.year,
            'month' : self.created.strftime("%m"),
            'slug' : self.slug
        })
    
    
    @property
    def img(self):
        if not self.IMG_CACHE:
            try:
                self.IMG_CACHE = self.photo_set.all()[0]
            except IndexError:
                pass
        return self.IMG_CACHE
    

class Photo(models.Model):
    post = models.ForeignKey(Post, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    license_url = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=255,blank=True, null=True )
    created = models.DateTimeField(auto_now_add=True)
    photo = ImageWithThumbsField(upload_to='uploads/photo/%Y/%m/%d', sizes=settings.PHOTO_SIZES)
    
    def __unicode__(self):
        return u'Photo : %s' % self.pk
    
    @property
    def t(self):
        try:
            return self.photo.url_100x100
        except AttributeError:
            return False
        
    
    @property
    def s(self):
        try:
            return self.photo.url_155x100
        except AttributeError:
            return False
    
    def m(self):
        try:
            return self.photo.url_240x160
        except AttributeError:
            return False
    
    def l(self):
        try:
            return self.photo.url_290x248
        except AttributeError:
            return False
    
    def f(self):
        try:
            return self.photo.url_800x600
        except AttributeError:
            return False
    
    def xl(self):
        try:
            return self.photo.url_2560x1440
        except AttributeError:
            return False
    
#
#
# South
rules = [
    (
        (ImageWithThumbsField, ),
        [],
        {
            "blank": ["blank", {"default": True}],
            "max_length": ["max_length", {"default": 100}],
        },
    ),
]
add_introspection_rules(rules, ["^apps\.utils\.fields",])

