from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'eldar.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

     #url(r'^$', 'eldar.views.home', name='home'),
     #url(r'^vaktir$', 'vaktir.views.yfirlit', name='yfirlit'),
     url(r'^vaktir$', 'vaktir.views.skraning', name='skraning'),
     url(r'^vaktir/skra$', 'vaktir.views.skra', name='skra'),
     url(r'^vaktir/umsjon$', 'vaktir.views.umsjon', name='umsjon'),
     #url(r'^vaktir/smidi$', 'vaktir.views.smidi', name='smidi'),
     #url(r'^vaktir/skraning$', 'vaktir.views.skraning', name='skraning'),
     #url(r'^vaktir/umsjon$', 'vaktir.views.umsjon', name='yfirlit'),

     url(r'^lager$', 'lager.views.yfirlit', name='yfirlit'),
     url(r'^lager/verdmidar$', 'lager.views.verdmidar', name='verdmidar'),

    url(r'^admin/', include(admin.site.urls)),
]
