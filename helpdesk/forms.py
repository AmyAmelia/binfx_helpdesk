from datetime import datetime
from django import forms
from .models import *
from django.contrib.auth.models import User, Group

class RaiseIssueForm(forms.ModelForm):
    ''' Form for raising an new issue with Bioinformatics'''
    class Meta:
        model = Issue
        fields = ('issue','type','is_urgent','description')

class AddCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddCommentForm, self).__init__(*args, **kwargs)
    class Meta:
        model = IssueComment
        fields = ['comment']

class IssueUpdateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['status', 'assignee']

    def __init__(self, *args, **kwargs):
        super(IssueUpdateForm, self).__init__(*args, **kwargs)
        # restrict assignee selection to members of the bioinformatics team
        self.fields['assignee'].queryset = User.objects.filter(groups__name='bioinformatician')