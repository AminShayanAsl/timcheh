from django.conf.urls import url
from . import views

app_name = 'timcheh'

urlpatterns = [
    url('^source_products/$', views.source_products, name='mobiles_list'),
]
