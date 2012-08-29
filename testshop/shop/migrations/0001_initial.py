# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Designer'
        db.create_table('shop_designer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('avatar', self.gf('django_thumbs.db.models.ImageWithThumbsField')(default='', max_length=100, sizes=((40, 40), (50, 50), (100, 100), (200, 200)))),
        ))
        db.send_create_signal('shop', ['Designer'])

        # Adding model 'ProductImage'
        db.create_table('shop_productimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('version', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, null=True, blank=True)),
            ('fpath', self.gf('django_thumbs.db.models.ImageWithThumbsField')(default='', max_length=100, sizes=((50, 50), (100, 100), (200, 200), (400, 400)))),
        ))
        db.send_create_signal('shop', ['ProductImage'])

        # Adding model 'Product'
        db.create_table('shop_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, blank=True)),
            ('sort', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, null=True, blank=True)),
            ('designer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Designer'], null=True, blank=True)),
            ('category', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='products', null=True, to=orm['shop.Category'])),
        ))
        db.send_create_signal('shop', ['Product'])

        # Adding M2M table for field images on 'Product'
        db.create_table('shop_product_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['shop.product'], null=False)),
            ('productimage', models.ForeignKey(orm['shop.productimage'], null=False))
        ))
        db.create_unique('shop_product_images', ['product_id', 'productimage_id'])

        # Adding model 'Category'
        db.create_table('shop_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(to=orm['shop.Category'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('img', self.gf('django.db.models.fields.URLField')(default='/media/img/products/product_1.jpg', max_length=200, blank=True)),
        ))
        db.send_create_signal('shop', ['Category'])

        # Adding model 'ContactInfo'
        db.create_table('shop_contactinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('phone_num', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=55)),
            ('area_design', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('shop', ['ContactInfo'])


    def backwards(self, orm):
        # Deleting model 'Designer'
        db.delete_table('shop_designer')

        # Deleting model 'ProductImage'
        db.delete_table('shop_productimage')

        # Deleting model 'Product'
        db.delete_table('shop_product')

        # Removing M2M table for field images on 'Product'
        db.delete_table('shop_product_images')

        # Deleting model 'Category'
        db.delete_table('shop_category')

        # Deleting model 'ContactInfo'
        db.delete_table('shop_contactinfo')


    models = {
        'shop.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.URLField', [], {'default': "'/media/img/products/product_1.jpg'", 'max_length': '200', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['shop.Category']", 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'shop.contactinfo': {
            'Meta': {'object_name': 'ContactInfo'},
            'area_design': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '55'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone_num': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'shop.designer': {
            'Meta': {'object_name': 'Designer'},
            'avatar': ('django_thumbs.db.models.ImageWithThumbsField', [], {'default': "''", 'max_length': '100', 'sizes': '((40, 40), (50, 50), (100, 100), (200, 200))'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'shop.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'products'", 'null': 'True', 'to': "orm['shop.Category']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Designer']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['shop.ProductImage']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'sort': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'})
        },
        'shop.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'fpath': ('django_thumbs.db.models.ImageWithThumbsField', [], {'default': "''", 'max_length': '100', 'sizes': '((50, 50), (100, 100), (200, 200), (400, 400))'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['shop']