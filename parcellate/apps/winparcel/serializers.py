from django.forms import widgets
from rest_framework import serializers
from .models import Collection, Widget

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('url', 'uuid', 'title',  'published',
                  'updated', 'column', 'row', 'collection_type')


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ('url', 'uuid', 'title', 'published',
                  'updated', 'column', 'row', 'widget_type', 'collection',
                  'srcid', 'summary', 'content')
