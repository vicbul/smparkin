from django.conf.urls import url
from django.views.generic.base import TemplateView


from resources import views

urlpatterns = [
    # url(r'^$', views.subscription, name='subs'),
    url(r'^', TemplateView.as_view(template_name='resources/home.html'), name='home'),
]