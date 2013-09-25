from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import (View,
                                  CreateView,
                                  UpdateView,
                                  DetailView)
from .models import RSSObject
from .lib import ReadRSS

class ParcelView(View):
    template_name = "parcel.html"

    def get(self, request):
        rss_objects = RSSObject.objects.all()
        return render(request,
                      self.template_name,
                      dict(test="TEST",
                           rss_objects=rss_objects)
                     )



class RSSObjectCreateView(CreateView):
    model = RSSObject
    template_name = "add_rss.html"

    def form_valid(self, form):
        response = super(RSSObjectCreateView, self).form_valid(form)
        read_rss = ReadRSS(rss=self.object)
        read_rss.save_entries()
        return response


    def get_success_url(self):
        return reverse("rss-add")

    def get_context_data(self, **kwargs):
        context = super(RSSObjectCreateView, self).get_context_data(**kwargs)
        context["object_list"] = RSSObject.objects.all()
        return context


class RSSObjectUpdateView(UpdateView):
    model = RSSObject
    template_name = "add_rss.html"

    def get_success_url(self):
        slug = self.kwargs.get('pk', None)
        if slug:
            return reverse('rss-update', kwargs=dict(pk=slug))
        return reverse("rss-add")

    def get_context_data(self, **kwargs):
        context = super(RSSObjectUpdateView, self).get_context_data(**kwargs)
        context["object_list"] = RSSObject.objects.all()
        return context


class RSSObjectDetailView(DetailView):
    model = RSSObject
    template_name = "show_rss.html"
