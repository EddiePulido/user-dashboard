from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^login_page$', views.login_page),
    url(r'^register$', views.register_page),
    url(r'^users/edit$', views.edit_profile),
    url(r'^users/edit/(?P<id>\d+)$', views.edit_admin),
    url(r'^users/show/(?P<id>\d+)$', views.show_user),
    url(r'^dashboard$', views.dashboard),
    url(r'^dashboard/admin$', views.dashboard_admin),
    url(r'^users/new$', views.new_user),
    url(r'^post_message$', views.post_message),
    url(r'^post_comment$', views.post_comment),
    url(r'^remove/(?P<id>\d+)$', views.remove_user),
    url(r'^update_password/(?P<id>\d+)$',views.update_password),
    url(r'^update_user/(?P<id>\d+)$', views.update_user),
    url(r'^delete_message/(?P<id>\d+)$', views.delete_message),
    url(r'^delete_comment/(?P<id>\d+)/(?P<user_id>\d+)$', views.delete_comment),
]