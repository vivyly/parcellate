from django.shortcuts import render
from django.views.generic import (View,
                                  CreateView,
                                  UpdateView,
                                  DetailView)
from .models import RSSObject

class ParcelView(View):
    template_name = "entry.html"

    def get(self, request):
        rss_objects = RSSObject.objects.all()
        return render(request,
                      self.template_name,
                      dict(rss_objects=rss_objects))



class RSSObjectCreateView(CreateView):
    model = RSSObject
    action = "created"


class RSSObjectUpdateView(UpdateView):
    model = RSSObject
    action = "updated"


class RSSObjectDetailView(DetailView):
    model = RSSObject
