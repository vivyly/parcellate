from django.forms import widgets
from rest_framework import serializers
from .models import Collection, Widget

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('url', 'pk', 'uuid', 'title', 'summary', 'published',
                  'updated', 'content', 'column', 'row')


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = ('url', 'pk', 'uuid', 'title', 'published',
                  'updated', 'column', 'row')
