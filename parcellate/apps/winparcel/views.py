
from django.template import RequestContext
from django.shortcuts import render_to_response

def parcel(request):
    col1 = ['www.google.com','www.bing.com', 'www.freakonomics.com']
    col2 = ['www.pajiba.com', 'www.reddit.com', 'news.ycombinator.com/news']
    col3 = ['www.seriouseats.com', 'sf.eater.com']
    return render_to_response('parcel.html', 
            {
                'col1':col1,
                'col2':col2,
                'col3':col3
            }, context_instance=RequestContext(request))
