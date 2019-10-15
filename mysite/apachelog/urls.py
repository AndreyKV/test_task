from django.urls import path

from apachelog.views import ApacheLogListView

urlpatterns = [
    path('', ApacheLogListView.as_view(), name='apachelog-list'),
]
