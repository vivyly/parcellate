from django import forms

from .models import RSSObject


class AddRSSForm(forms.Form):
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


#class AddRSSEntryForm(forms.Form):


