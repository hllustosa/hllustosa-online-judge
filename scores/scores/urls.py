from django.contrib import admin
from django.conf.urls import url 
from api.views import ScoreListView, ScoreDetailsListView


urlpatterns = [
    url(r'^api/scores/all$', ScoreListView.as_view()),
    url(r'^api/scores/(?P<pk>.*)$', ScoreDetailsListView.as_view()),
]
