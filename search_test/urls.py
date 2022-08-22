from django.conf.urls import include, url
from django.urls import path
from tastypie.api import Api
from .app import DataResource

# v1_api = Api(api_name='v1')
# v1_api.register(DataResource)
data_resource = DataResource()

urlpatterns = [
    url(r'api/', include(data_resource.urls)),
]