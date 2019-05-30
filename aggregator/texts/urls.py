from django.urls import path
from . import views

urlpatterns = [
    path('', views.TextsView.as_view()),
    path('page/<int:page_number>/', views.TextsView.as_view()),
    path('check/', views.StartCheck.as_view()),
    path('check/<int:pk>/', views.TextView.as_view(), kwargs={'new': False}),
    path('check/<int:pk>/new/', views.TextView.as_view(), kwargs={'new': True}, name='detail_view')
]
