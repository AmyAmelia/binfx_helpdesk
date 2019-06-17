from django.urls import path
from . import views

urlpatterns = [
    path('',views.view_issues, name = 'view_issue'),
    path('issue/<int:record_id>/',views.issue_description, name='issue_description'),
    path('issue/new', views.issue_new, name='issue_new'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete-comment'),
    path('edit_comment/<int:comment_id>', views.edit_comment, name='edit-comment'),
    path('update_issue/<int:issue_id>', views.update_issue, name='update-issue')
]