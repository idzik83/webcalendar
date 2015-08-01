from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webcalendar.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^geteventlist$', views.get_event_list, name='get_event_list'),
    url(r'^save$', views.save_events, name='save_events'),
    url(r'^delevent$', views.delete_event, name='delete_event'),
)
