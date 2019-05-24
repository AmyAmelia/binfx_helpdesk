from django.urls import path
from . import views

urlpatterns = [
    path('',views.view_issues, name = 'view_issue'),
    path('issue/<int:pk>/',views.issue_description, name='issue_description'),
    path('issue/new', views.issue_new, name='issue_new'),

]