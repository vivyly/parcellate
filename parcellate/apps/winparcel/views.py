
from django.template import RequestContext
from django.shortcuts import render_to_response
from .lib import ParcelFactory


def parcel(request):
    col1 = ['www.google.com','www.bing.com', 'www.freakonomics.com']
    col2 = ['www.pajiba.com', 'www.reddit.com', 'news.ycombinator.com/news']
    col3 = ['www.seriouseats.com', 'sf.eater.com']
    parcel_factory = ParcelFactory(col1, col2, col3)
    return render_to_response('parcel.html',
            dict(factory=parcel_factory),
            context_instance=RequestContext(request))
