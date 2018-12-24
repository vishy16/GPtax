from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from extra import views as extra_views
from django.contrib.auth import views

urlpatterns = [
    url(r'^accounts/login/$', views.login,{'template_name': 'registration/login.html'}, name='login'),
    url(r'^accounts/logout/$', views.logout, {'next_page': '/'}, name='logout'),

    url(r'^accounts/password_change/$',
        views.password_change, {'template_name': 'registration/password_change.html'}, name='password_change'),
    url(r'^accounts/password_change/done/$',
        views.password_change_done,{'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
    url(r'^accounts/password_reset/$',
        views.password_reset, {'template_name': 'registration/password_reset.html'}, name='password_reset'),
    url(r'^accounts/password_reset/done/$',
        views.password_reset_done, {'template_name': 'registration/password_reset_done_one.html'}, name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,{'template_name': 'registration/password_reset_confirmed.html'}, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$',
        views.password_reset_complete,{'template_name': 'registration/password_reset_completed.html'}, name='password_reset_complete'),

    url(r'^$', extra_views.home,name = 'home'),
    url(r'^base$', extra_views.base,name = 'base'),
    url(r'^extra/', include('extra.urls',namespace = 'extra')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pay_online/', include('payonline.urls',namespace = 'payonline')),
    #url(r'^registration/', include('registration.urls',namespace = 'registration')),
    url(r'^amnesty_scheme/', include('amnestyscheme.urls',namespace= 'amnestyscheme')),
    url(r'^taxbill/', include('taxbill.urls',namespace = 'taxbill')),
    url(r'^tax_reciept/', include('taxreciept.urls',namespace = 'taxreciept')),
    url(r'^getnoc/', include('getnoc.urls',namespace = 'getnoc')),
    url(r'^helpdesk/', include('helpdesk.urls',namespace = 'helpdesk')),
    url(r'^collection_center/', include('collectioncenter.urls',namespace = 'collectioncenter')),
    url(r'^reports/', include('reports.urls',namespace = 'reports')),
    url(r'^property_details/', include('propertydetails.urls',namespace = 'propertydetails')),
    url(r'^payment/', include('paymentgateway.urls',namespace = 'payment')),
    url(r'accounts/', include('accounts.urls', namespace='accounts')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
