from django.urls import path, re_path
from config.constants import message_id_length
from . import views

urlpatterns = [
    path('check/', views.CheckText.as_view()),
    path('check/readonly/', views.ReadonlyResponse.as_view(), name='readonly'),
    re_path(r'^result/(?P<message_id>[a-z0-9]{%s})/$' % message_id_length, views.ModelingResult.as_view())
]
