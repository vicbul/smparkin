from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from resources.models import test

# Create your views here.

def subscription(request):
    #print 'request', request
    return render(request, 'resources/subscriptions.html')

def test(request):

    return render_to_response("test.html",
                          {'nodes':test.objects.all()},
                          context_instance=RequestContext(request))