from django.conf.urls import url
from subcity import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
]