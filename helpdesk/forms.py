from datetime import datetime
from django import forms
from .models import *
from django.contrib.auth.models import User, Group

class RaiseIssueForm(forms.ModelForm):
    ''' Form for raising an new issue with Bioinformatics'''
    class Meta:
        model = Issue
        # NOTE: if fields are added/ edited, update the 'def save' function below
        fields = ('issue','type','is_urgent','description', 'collaborators')

    def save(self, request):
        '''Manual saving of new issues, to permit the m2m collaborators field. '''
        new_issue = self.instance
        new_issue.issue = self.cleaned_data['issue']
        new_issue.type = self.cleaned_data['type']
        new_issue.is_urgent = self.cleaned_data['is_urgent']
        new_issue.description = self.cleaned_data['description']

        # assign test status to 'Pending" and capture who and when raised the issue.
        new_issue.creator = request.user
        new_issue.status = Status.objects.get(status='Pending')
        new_issue.open = timezone.now()
        new_issue.save()
        # save collaborators.
        for colab in self.cleaned_data['collaborators']:
            # colab = User.objects.get(username=colab)
            # print (colab)
            new_issue.collaborators.add(colab)
        print (new_issue.id)
        return new_issue.id

                #
                #
                # def save(self, request):
                #     sample_report = self.instance
                #     sample_report.save()
                #     sample_panels = SamplePanel.objects.filter(sample_report=sample_report)
                #     for sample_panel in sample_panels:
                #         if sample_panel.panel_version not in self.cleaned_data['panels']:
                #             sample_panel.delete()
                #     for panel in self.cleaned_data['panels']:
                #         SamplePanel.objects.get_or_create(sample_report=sample_report,
                #                                           panel_version=panel,
                #                                           defaults={'added_by': request.user})

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