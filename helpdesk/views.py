from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.utils import timezone
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.db.models import Q


# Create your views here.

def view_issues(request):
    ''' Opening dashboard view listing all Open issues'''
    # closed issues are defined by the closed date not being null'
    closed_issues = Issue.objects.filter(closed_date__isnull=False)
    # If no closed date, issue is assumed to be open
    open_issues = Issue.objects.filter(closed_date__isnull=True)
    return render(request, 'helpdesk/view_issue.html',{'closed_issues':closed_issues, 'open_issues':open_issues})


def issue_description(request, pk):
    ''' Detailed description of individual issue and ability to comment on issue'''
    issue = get_object_or_404(Issue, pk=pk)
    add_comment_form = AddCommentForm(user=request.user)
    if request.method == "POST":
        if 'add_comment' in request.POST:
            add_comment_form = AddCommentForm(request.POST)
            if add_comment_form.is_valid():
                IssueComment.objects.create(issue_record=issue,
                                           comment=add_comment_form.cleaned_data['comment'],
                                           user=request.user,
                                           time=timezone.now())
    return render(request, 'helpdesk/issue_description.html', {'issue': issue,
                                                               'add_comment_form': add_comment_form})

def issue_new(request):
    if request.method == "POST":
        issue_form = RaiseIssueForm(request.POST)
        if issue_form.is_valid():
            Issue = issue_form.save(commit=False)
            Issue.creator = request.user
            Issue.status = Status.objects.get(status='Pending')
            Issue.open = timezone.now()
            Issue.save()
            return redirect('issue_description', pk=Issue.pk)
    else:
        issue_form = RaiseIssueForm()
    return render(request, 'helpdesk/issue_new.html',{'issue_form': issue_form})

# @login_required
def delete_comment(request, comment_id):
    comment = IssueComment.objects.get(id=comment_id)
    linked_issue = comment.issue_record
    comment.delete()
    return HttpResponseRedirect(f'/issue/{linked_issue.id}')

# TODO: Add in IssueComments Form View
# TODO: Add in functionality to email bioinformatics when 1) a new issue is raised. 2) a non-binfx user adds a comment
# TODO: email issue owner when status is changed/ comment is made
# TODO: Add function for Bifx to change status, close issue