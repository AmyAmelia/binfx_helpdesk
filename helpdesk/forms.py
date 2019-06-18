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
        self.user = kwargs.pop('user', None)
        super(IssueUpdateForm, self).__init__(*args, **kwargs)
        # restrict assignee options to members of the bioinformatics team only
        self.fields['assignee'].queryset = User.objects.filter(groups__name='bioinformatician')
        # restrict updating issue status/ assignee to bioinformaticians only.
        print(self.user)
        if not self.user.groups.first().name == 'bioinformatician':
            for field in self.fields:
                self.fields[field].disabled = True