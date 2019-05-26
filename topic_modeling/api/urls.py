from django.urls import path, re_path
from config.constants import message_id_length
from . import views

urlpatterns = [
    path('check/', views.CheckText.as_view()),
    re_path(r'^result/(?P<message_id>[a-z0-9]{%s})/$' % message_id_length, views.ModelingResult.as_view())
]
