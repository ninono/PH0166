from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from pslechweb.views import *
from pslechweb.output import *
from pslechweb.account import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pslech.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^redactor/', include('redactor.urls')),

    url(r'^$',welcome),
    url(r'^home/$',home),
    url(r'^accounts/login/$',account_login),
    url(r'^accounts/logout/$',account_logout),
    url(r'^accounts/register/$',account_register),
    url(r'^accounts/activate/$',account_activate),
    url(r'^accounts/forgot/$',account_forgot),
    url(r'^accounts/reset/$',account_reset),
    url(r'^accounts/profile/$',RedirectView.as_view(url='/home/')),

    url(r'^practice/$',practice_home),
    url(r'^practice/(?P<part>P(1|2))/(?P<section>S(A|B))/$',practice_select_section),
    url(r'^practice/(?P<part>P(1|2))/(?P<section>S(A|B))/topic(?P<topicId>\w+)/$',practice_select_section),
    url(r'^practice/(?P<part>P(1|2))/(?P<section>S(A|B))/(?P<passage_id>\d+)/$',practice_passage),
    #url(r'^practice/(?P<part>P(1|2))/(?P<section>S(A|B))/(?P<section_id>\d+)/result$',mark),
    url(r'^mark/$',mark),

    url(r'^CATPractice/$',select_cat_qTag),
    url(r'^CATPractice/(\d+)/$',cat_practice),
#

    #url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    url(r'^tip/$',display_tip),
    url(r'^download/$',download_csv),
)
from django.conf import settings
from django.contrib.staticfiles import views
if settings.DEBUG:
    urlpatterns+=[
            url(r'^static/(?P<path>.*)$', views.serve),
            ]

# Append staticfiles into urlpatterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

