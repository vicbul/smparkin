from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.generic import View

# Create your views here.

def subscription(request):
    #print 'request', request
    return render(request, 'resources/subscriptions.html')

# View to display get or post data
# class MyView(View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse('This is GET request')
#
#     def post(self, request, *args, **kwargs):
#         return HttpResponse('This is POST request')



