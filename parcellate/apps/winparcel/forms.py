from django import forms

from .models import (Collection,
                     Parcel)


class AddFeedburnerForm(forms.Form):
    rss_url = forms.URLField(required=False)
    name = forms.CharField(required=False)

    def clean_name(self):
        data = self.cleaned_data
        name = data.get('name')
        return 'http://feeds.feedburner.com/%s' % name

    def clean(self):
        data = self.cleaned_data
        rss_url = data.get('rss_url')
        if not rss_url:
            data['rss_url'] = data.get('name')
        return data

    def save(self):
        data = self.cleaned_data
        rss_obj = RSSObject()
        rss_obj.atom = data.get('rss_url')
        rss_obj.save()
        return rss_obj


    def get_domain_object(self):
        from .models import Collection
        domain_url = self.find_domain_url()
        try:
            c = Collection.objects.get(url=domain_url)
        except Collection.DoesNotExist:
            c = self.create_collection(domain_url)
        return c

    def create_collection_type(self, name):
        from .models import CollectionType
        ctype = CollectionType()
        ctype.name = name
        ctype.save()
        return ctype

    def create_widget_type(self, name):
        from .models import WidgetType
        wtype = WidgetType()
        wtype.name = name
        wtype.save()
        return wtype

    def create_collection(self, domain_url):
        from .models import Collection
        ctype = self.create_collection_type(self.collection_type)
        c = Collection()
        c.url = domain_url
        c.title = self.collection_title or domain_url
        c.status = 'active'
        c.collection_type = ctype
        c.save()
        return c
