from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
	url(r'^$',views.TemplateProcess.as_view(), name = 'Main page'),
	url(r'^opp13/$',views.TemplateProcess.as_view(), name = 'Main page'),
	url(r'^process_steps/$',views.DataAjax.as_view(), name = 'Step ajax'),
	url(r'^process/$',views.DataProcess.as_view(), name = 'Data process'),
	url(r'^create/$',views.Create.as_view(), name = 'Create'),
	url(r'^loadNumerals/$',views.loadNumerals.as_view(), name = 'loadNumerals'),
]
