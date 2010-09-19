# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Book.tags'
        db.add_column('books_book', 'tags', self.gf('tagging.fields.TagField')(default=' '), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Book.tags'
        db.delete_column('books_book', 'tags')


    models = {
        'books.book': {
            'Meta': {'object_name': 'Book'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'photo': ('apps.utils.fields.ImageWithThumbsField', [], {'blank': 'False'}),
            'purchased': ('django.db.models.fields.DateField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['books']