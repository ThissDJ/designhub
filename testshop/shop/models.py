# encoding: utf-8
import datetime,os
from django.db import models, IntegrityError
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext as _
from testshop import settings
from plugshop.models import ProductAbstract, CategoryAbstract
from django_thumbs.db.models import ImageWithThumbsField
from paypal.standard.ipn.signals import payment_was_successful
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([
        (
            [ImageWithThumbsField], # Class(es) these apply to
            [],         # Positional arguments (not used)
            {           # Keyword argument
                "sizes": ["sizes", {}],
            },
        ),
    ], ["^django_thumbs\.db\.models\.ImageWithThumbsField"])

UPLOADED_TO = os.path.join(settings.MEDIA_ROOT,settings.UPLOAD_URI)


class Designer(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(_('slug'), blank=False, unique=True)
    description = models.TextField(blank=True)
    avatar = ImageWithThumbsField(upload_to=UPLOADED_TO, sizes=((40,40),(50,50),(100,100),(200,200),(400,400),(630,630)),default='')
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('designer-detail', None, {
            'slug': self.slug,
        })
    def save(self):
        """Auto-populate an empty slug field from the MyModel name and
        if it conflicts with an existing slug then append a number and try
        saving again.
        """
        import re
        from django.template.defaultfilters import slugify
        
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        while True:
            try:
                super(Designer, self).save()
            # Assuming the IntegrityError is due to a slug fight
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break
class DesignerCreateForm( ModelForm ) :
    class Meta :
        model = Designer
        fields = (
            'name',
            'description',
            'avatar',
        )
        widgets = {
            'description': Textarea(attrs={'class':'redactor-textarea'
                                           ,'name':'content','height':"200px"}),
        }


class ProductImage(models.Model):
    version = models.PositiveIntegerField(blank=True, null=True, default=1)
    fpath = ImageWithThumbsField(upload_to=UPLOADED_TO, sizes=((50,50),(100,100),(200,200),(400,400),(630,630)),default='')
    
    def __unicode__(self):
        return str(self.id)

class Category(CategoryAbstract):
    description = models.TextField(blank=True)
    img = models.URLField(blank=True,default="/media/img/products/product_1.jpg")

class Product(ProductAbstract):
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(blank=True, null=True,default=datetime.datetime.now)
    finish = models.DateTimeField(blank=True, null=True,default=datetime.datetime.now)
    time_discount = models.BooleanField(default=False)
    sort = models.PositiveIntegerField(blank=True, null=True, default=1)
    images = models.ManyToManyField(ProductImage)
    designer = models.ForeignKey(Designer,blank=True, null=True)
    idea = models.TextField(blank=True,null=True,default="")
    delivery = models.TextField(blank=True,null=True,default="")
    original_price = models.FloatField(blank=True,null=True,default=0.0)
#    category = models.ForeignKey(Caterogry,blank=True, null=True)
    def __unicode__(self):
        return self.name

    def save(self):
        """Auto-populate an empty slug field from the MyModel name and
        if it conflicts with an existing slug then append a number and try
        saving again.
        """
        import re
        from django.template.defaultfilters import slugify
        
        if not self.slug:
            self.slug = slugify(self.name)  # Where self.name is the field used for 'pre-populate from'
        while True:
            try:
                super(Product, self).save()
            # Assuming the IntegrityError is due to a slug fight
            except IntegrityError:
                match_obj = re.match(r'^(.*)-(\d+)$', self.slug)
                if match_obj:
                    next_int = int(match_obj.group(2)) + 1
                    self.slug = match_obj.group(1) + '-' + str(next_int)
                else:
                    self.slug += '-2'
            else:
                break
    def checkStorage(self,size='Average'):
        if size == 'Average':
            storages = Storage.objects.filter(product = self, num__gte = 0)
        else:
            storages = Storage.objects.filter(product = self, size = size, num__gte = 0)
        if self.time_discount:
            if self.finish.replace(tzinfo = None) > datetime.datetime.now():
                return storages
            else:
                return []
        else:
            return storages
        
    def restTime(self):
        if self.time_discount and self.finish.replace(tzinfo = None) > datetime.datetime.now(): 
            diff = self.finish.replace(tzinfo = None) - datetime.datetime.now()
            second_diff = diff.seconds
            day_diff = diff.days
            if day_diff < 0:
                return ''
            if day_diff == 0:
                if second_diff < 10:
                    return "a second"
                if second_diff < 60:
                    return str(second_diff) + " seconds"
                if second_diff < 120:
                    return  "a minute"
                if second_diff < 3600:
                    return str( second_diff / 60 ) + " minutes"
                if second_diff < 7200:
                    return "an hour"
                if second_diff < 86400:
                    return str( second_diff / 3600 ) + " hours"
            if day_diff == 1:
                return "one day"
            if day_diff < 365:
                return str(day_diff) + " days"
            return str(day_diff/365) + " years"
        else:
            return ''

class ProductUpdateForm( ModelForm ) :
    class Meta :
        model = Product
        fields = (
            'name',
            'slug',
            'price',
            'idea',
            'description',
            'delivery',
            'sort',
        )
        widgets = {
            'idea': Textarea(attrs={'class':'redactor-textarea'
                                           ,'name':'content','height':"200px"}),
            'description': Textarea(attrs={'class':'redactor-textarea'
                                           ,'name':'content','height':"200px"}),
            'delivery': Textarea(attrs={'class':'redactor-textarea'
                                           ,'name':'content','height':"200px"}),
        }

class ContactInfo(models.Model):
    name = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=20)
    email = models.EmailField(max_length=55)
    area_design = models.CharField(max_length=80)
    
    def __unicode__(self):
        return self.name

class ContactInfoForm( ModelForm ) :
    class Meta :
        model = ContactInfo

class Storage(models.Model):
    product = models.ForeignKey(Product)
    size = models.CharField(max_length=20,blank=True, null=True)
    num = models.IntegerField(blank=False, null=False, default=1)
    
    def __unicode__(self):
        return str(self.product.name)

class Comment(models.Model):
    product = models.ForeignKey(Product,blank=False, null=False)
    user = models.ForeignKey(User,blank=True, null=True)
    content = models.TextField(blank=True)
    created = models.DateTimeField(default=datetime.datetime.now,blank=True, null=True, auto_now_add = True)
    def __unicode__(self):
        return self.product.name

class ProductCommentForm( ModelForm ) :
    class Meta :
        model = Comment
        fields = (
            'content',
        )


from paypal.standard.ipn.signals import payment_was_successful

def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    # Undertake some action depending upon `ipn_obj`.
    if ipn_obj.custom == "Upgrade all users!":
        Users.objects.update(paid=True)
    import sys
    print >>sys.stderr, 'Goodbye, cruel worldddddddddddddddddddddddddddd!'       
payment_was_successful.connect(show_me_the_money)


class StaticSitemap(Sitemap):
    
    priority = 0.8
    lastmod = datetime.datetime.now()
    
    def __init__(self, filename):
        import re,string
        self._urls = []
        try:
            f = open(filename, 'rb')
        except:
            return
        
        tmp = []
        for x in f:
            x = re.sub(r"\s*#.*$", '', x) # strip comments
            if re.match('^\s*$', x):
                continue # ignore blank lines
            x = string.strip(x) # clean leading/trailing whitespace
            x = re.sub(' ', '%20', x) # convert spaces
            if not x.startswith('/'):
                x = '/' + x
            tmp.append(x)
        f.close()
        self._urls = tmp
    # __init__
    
    def items(self):
        return self._urls
    
    def location(self, obj):
        return obj
from plugshop.models.order_products import OrderProductsAbstract
from plugshop.utils import load_class
from plugshop.models.order import Order
class OrderProductsSize(OrderProductsAbstract):
    class Meta:
        app_label = 'plugshop'
        verbose_name = _('order product with size')
        verbose_name_plural = _('order product with size')
    size = models.CharField(max_length=20,blank=True, null=True)
