from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import (View,
                                  CreateView,
                                  UpdateView,
                                  DetailView)
from .models import RSSObject
from .lib import ReadRSS

COLUMNS = 3 #will later be set by a manager, 3 for now though

class ParcelView(View):
    template_name = "parcel.html"

    def get(self, request):
        rss_objects = RSSObject.objects.all()
        obj_cols = dict([(x, []) for x in range(0, COLUMNS)])
        for idx, rss_object in enumerate(rss_objects):
            obj_cols[idx] = rss_object
        return render(request,
                      self.template_name,
                      dict(test="TEST",
                           obj_cols=obj_cols)
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
