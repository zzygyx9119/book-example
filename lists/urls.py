from django.conf.urls import url

from lists import views

urlpatterns = [
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^(\d+)/items/$', views.list_items, name='list_items'),
    url(r'^(\d+)/items/add$', views.add_to_list, name='add_to_list'),
    url(r'^users/(.+)/$', views.my_lists, name='my_lists'),
]

