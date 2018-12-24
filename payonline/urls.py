from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^prop_dues_details$', views.payonline_base, name='payonline_base'),
]