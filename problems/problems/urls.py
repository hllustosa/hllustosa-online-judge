from django.contrib import admin
from django.urls import path
from django.conf.urls import url 
from api.views import ProblemsListView, ProblemsDetailsView, RunsListView, RunsAllListView, RunsDetailsView

urlpatterns = [
    url(r'^api/problems$', ProblemsListView.as_view()),
    url(r'^api/runs$', RunsListView.as_view()),
    url(r'^api/runs/all$', RunsAllListView.as_view()),
    url(r'^api/problems/(?P<pk>.*)$', ProblemsDetailsView.as_view()),
    url(r'^api/runs/(?P<pk>.*)$', RunsDetailsView.as_view()),
]
