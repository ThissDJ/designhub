from django.db import models
from django.utils.translation import ugettext_lazy as _
from product.models import Product
from product.models import Discount
from satchmo_utils.thumbnail.field import ImageWithThumbnailField
from satchmo_store.contact.models import Contact

SATCHMO_PRODUCT=True

class Designer(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(_('slug'), blank=False, unique=True)
    description = models.TextField(blank=True)
    artist = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
#    avatar = ImageWithThumbsField(upload_to=UPLOADED_TO, sizes=((40,40),(50,50),(100,100),(200,200),(400,400),(630,630)),default='')
    def _get_mainImage(self):
        img = False
        if self.designerimage_set.count() > 0:
            img = self.designerimage_set.order_by('sort')[0]
        else:
            try:
                img = DesignerImage.objects.filter(designer__isnull=True).order_by('sort')[0]
            except IndexError:
                import sys
                print >>sys.stderr, 'Warning: default designer image not found - try syncdb'

        return img

    main_image = property(_get_mainImage)

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

class Brand(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(_('slug'), blank=False, unique=True)
    description = models.TextField(blank=True)
    designer = models.ForeignKey(Designer, null=True, blank=True)
##    avatar = ImageWithThumbsField(upload_to=UPLOADED_TO, sizes=((40,40),(50,50),(100,100),(200,200),(400,400),(630,630)),default='')
#    def _get_mainImage(self):
#        img = False
#        if self.designerimage_set.count() > 0:
#            img = self.designerimage_set.order_by('sort')[0]
#        else:
#            try:
#                img = DesignerImage.objects.filter(designer__isnull=True).order_by('sort')[0]
#            except IndexError:
#                import sys
#                print >>sys.stderr, 'Warning: default designer image not found - try syncdb'
#
#        return img
#
#    main_image = property(_get_mainImage)

    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('brand-detail', None, {
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
                super(Brand, self).save()
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


class DesignerImage(models.Model):
    """
    A picture of an item.  Can have many pictures associated with an item.
    Thumbnails are automatically created.
    """
    designer = models.ForeignKey(Designer, null=True, blank=True)
    picture = ImageWithThumbnailField(verbose_name=_('Picture'),
        upload_to="__DYNAMIC__",
        name_field="_filename",
        max_length=200) #Media root is automatically prepended
    caption = models.CharField(_("Optional caption"), max_length=100,
        null=True, blank=True)
    sort = models.IntegerField(_("Sort Order"), default=0)

#    def translated_caption(self, language_code=None):
#        return lookup_translation(self, 'caption', language_code)

    def _get_filename(self):
        if self.designer:
            # In some cases the name could be too long to fit into the field
            # Truncate it if this is the case
            pic_field_max_length = self._meta.get_field('picture').max_length
            max_slug_length = pic_field_max_length -len('images/designerimage-picture-.jpg') - len(str(self.id))
            slug = self.designer.slug[:max_slug_length]
            return '%s-%s' % (slug, self.id)
        else:
            return 'default'
    _filename = property(_get_filename)

    def __unicode__(self):
        if self.designer:
            return u"Image of Designer %s" % self.designer.slug
        elif self.caption:
            return u"Image with caption \"%s\"" % self.caption
        else:
            return u"%s" % self.picture

    class Meta:
        ordering = ['sort']
        verbose_name = _("Designer Image")
        verbose_name_plural = _("Designer Images")



def get_product_types():
    """
    Returns a tuple of all product subtypes this app adds
    """
    return ('MyNewProduct', 'PreOrderProduct',)

class MyNewProduct(models.Model):
    product = models.OneToOneField(Product, verbose_name=_('Product'),
        primary_key=True)
    designer = models.ForeignKey(Designer, null=True, blank=True)
    brand = models.ForeignKey(Brand, null=True, blank=True)
    concept = models.TextField(null=True, blank=True, max_length=2000)
    preorder = models.BooleanField(default=False)
    end = models.DateTimeField(_("Preorder Ending Date"), null=True, blank=True)
    ship = models.TextField(null=True, blank=True, max_length=2000)
    featured = models.BooleanField(_("Featured"), default=False, help_text=_("Featured items will show on the front page"))
    def _get_subtype(self):
        """
        Has to return the name of the product subtype
        """
        return 'MyNewProduct'

    def __unicode__(self):
        return u"MyNewProduct: %s" % self.product.name

    class Meta:
        verbose_name = _('My New Product')
        verbose_name_plural = _('My New Products')

from tinymce import models as tinymce_models
class PreOrderProduct(models.Model):
    product = models.OneToOneField(Product, verbose_name=_('Product'),
        primary_key=True)
    designer = models.ForeignKey(Designer, null=True, blank=True)
    end = models.DateTimeField(_("Preorder Ending Date"), null=True, blank=True)
    description = models.TextField(null=True, blank=True, max_length=200)
    intro = tinymce_models.HTMLField(null=True, blank=True)
    ship = models.TextField(null=True, blank=True, max_length=2000)
    featured = models.BooleanField(_("Featured"), default=False, help_text=_("Featured items will show on the front page"))
    def _get_subtype(self):
        """
        Has to return the name of the product subtype
        """
        return 'PreOrderProduct'

    def __unicode__(self):
        return u"PreOrderProduct: %s" % self.product.name

    class Meta:
        verbose_name = _('Pre Order Product')
        verbose_name_plural = _('Pre Order Products')

class PreOrderImage(models.Model):
    """
    A picture of an item.  Can have many pictures associated with an item.
    Thumbnails are automatically created.
    """
    preorderproduct = models.ForeignKey(PreOrderProduct, null=True, blank=True)
    picture = ImageWithThumbnailField(verbose_name=_('Picture'),
        upload_to="__DYNAMIC__",
        name_field="_filename",
        max_length=200) #Media root is automatically prepended
    caption = models.CharField(_("Optional caption"), max_length=100,
        null=True, blank=True)
    sort = models.IntegerField(_("Sort Order"), default=0)

#    def translated_caption(self, language_code=None):
#        return lookup_translation(self, 'caption', language_code)

    def _get_filename(self):
        if self.preorderproduct:
            # In some cases the name could be too long to fit into the field
            # Truncate it if this is the case
            pic_field_max_length = self._meta.get_field('picture').max_length
            max_slug_length = pic_field_max_length -len('images/preorderproductposter-picture-.jpg') - len(str(self.id))
            slug = self.preorderproduct.product.slug[:max_slug_length]
            return '%s-%s' % (slug, self.id)
        else:
            return 'default'
    _filename = property(_get_filename)

    def __unicode__(self):
        if self.preorderproduct:
            return u"Image of PreOrderProductPoster %s" % self.preorderproduct.product.slug
        elif self.caption:
            return u"Image with caption \"%s\"" % self.caption
        else:
            return u"%s" % self.picture

    class Meta:
        ordering = ['sort']
        verbose_name = _("PreOrderProductPoster Image")
        verbose_name_plural = _("PreOrderProductPoster Images")


#
#from product.signals import index_prerender
#
#def add_brand_to_product(sender, **kwargs):
#    product_obj = sender
#    
##    ipn_obj = sender
##    # Undertake some action depending upon `ipn_obj`.
##    if ipn_obj.custom == "Upgrade all users!":
##        Users.objects.update(paid=True)
#    import sys
#    print >>sys.stderr, 'Good, cruel worldddddddddddddddddddddddddddd!'       
#index_prerender.connect(add_brand_to_product)


# invite friend to register, and give out coupon reword

class InviteReward(models.Model):
    invitor = models.ForeignKey(Contact, null=False, blank=False)
    invitees = models.ManyToManyField(Contact, related_name='u+')
    start_invite_date = models.DateTimeField(_("Start inviting Date"), null=True, blank=True, auto_now_add = True)
    discount = models.ForeignKey(Discount, null=True, blank=True)
    sent = models.BooleanField(default=False)
    sent_date = models.DateTimeField(_("Reward email sent date"), null=True, blank=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(_("Accepted the reward Date"), null=True, blank=True)
    def __unicode__(self):
        return u"Invitor: %s %s" %(self.invitor.first_name,self.invitor.last_name)
    