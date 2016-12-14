from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def subscription(request):
    #print 'request', request
    return render(request, 'resources/subscriptions.html')