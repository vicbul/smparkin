from django.conf.urls import url


from resources import views

urlpatterns = [
    url(r'^$', views.subscription, name='subs'),
]