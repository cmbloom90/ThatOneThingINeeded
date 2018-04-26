from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$',views.register),
	url(r'^login$',views.login),
	url(r'^logout$', views.logout),
	url(r'^dashboard$', views.dashboard),
	url(r'^wish_items/create$', views.create),
	url(r'^wish_items/create_item$', views.create_item),
	url(r'^wish_items/(?P<item_id>\d+)$', views.item),
	url(r'^add/(?P<item_id>\d+)$',views.add),
	url(r'^remove/(?P<item_id>\d+)$', views.remove),
]	