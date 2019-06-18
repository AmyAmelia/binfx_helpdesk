from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.utils import timezone
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse #, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q

@login_required
def view_issues(request):
    ''' Opening dashboard view summarising all issues. For non-bioinformaticians,
    view is restricted to issues raised by logged in user or issue user has been associated with'''
    if request.user.groups.first().name == 'bioinformatician':
        closed_issues = Issue.objects.filter(closed_date__isnull=False)
        # If no closed date, issue is assumed to be open
        open_issues = Issue.objects.filter(closed_date__isnull=True)
    else:
        # closed issues are defined by the closed date not being null'
        # closed_issues = Issue.objects.filter(closed_date__isnull=False, creator=request.user)
        closed_issues = Issue.objects.filter(Q(closed_date__isnull=False) & \
                             (Q(creator__username=request.user) | Q(collaborators__username=request.user)))
        # If no closed date, issue is assumed to be open
        open_issues = Issue.objects.filter(Q(closed_date__isnull=True) & \
                                           (Q(creator__username=request.user) | Q(collaborators__username=request.user)))
        # open_issues = Issue.objects.filter(closed_date__isnull=True, creator=request.user)
    return render(request, 'helpdesk/view_issue.html',{'closed_issues':closed_issues, 'open_issues':open_issues})

@login_required
def issue_description(request, record_id):
    #TODO: Allow issue creators to update issue discription?
    #TODO: Allow users to edit/ add collaborators
    ''' View displaying the detailed description of an individual issue
    with functionality to comment on issues, assign issues and update status.'''
    issue = get_object_or_404(Issue, pk=record_id)
    add_comment_form = AddCommentForm(user=request.user)
    issue_status_form = IssueUpdateForm(instance=issue, user=request.user)
    if request.method == "POST":
        if 'add_comment' in request.POST:
            add_comment_form = AddCommentForm(request.POST)
            if add_comment_form.is_valid():
                IssueComment.objects.create(issue_record=issue,
                                           comment=add_comment_form.cleaned_data['comment'],
                                           user=request.user,
                                           time=timezone.now())
    return render(request, 'helpdesk/issue_description.html', {'issue': issue,
                                                               'add_comment_form': add_comment_form,
                                                               'issue_status_form':issue_status_form})
@login_required
def issue_new(request):
    '''Raise a new issue to be addressed by the bioinformatics team'''
    issue_form = RaiseIssueForm()
    if request.method == "POST":
        issue_form = RaiseIssueForm(request.POST)
        # on submission assign test status to 'Pending" and capture who and when raised the issue.
        if issue_form.is_valid():
            id = issue_form.save(request)
            print(id)
            return redirect('issue_description', record_id=id)
    return render(request, 'helpdesk/issue_new.html',{'issue_form': issue_form})

@login_required
def update_issue(request, issue_id):
    '''Update an issue's status or assign issue to bioinformatician'''
    issue_update = get_object_or_404(Issue, pk=issue_id)
    if request.method == "POST":
        issue_update_form = IssueUpdateForm(request.POST, instance = issue_update, user=request.user)
        if issue_update_form.is_valid():
            issue_update = issue_update_form.save(commit=False)
            # Set an issue status to 'Assigned' when issue is first assigned.
            if issue_update_form.cleaned_data['assignee']:
                # Only update Status if it is currently set as Pending.
                if issue_update_form.cleaned_data['status'] == Status.objects.get(status='Pending'):
                    issue_update.status = Status.objects.get(status='Assigned')
            # If issue is closed (Status "Completed' or 'Not required', auto assign a closed date
            if issue_update_form.cleaned_data['status'] == Status.objects.get(status='Completed') \
                    or issue_update_form.cleaned_data['status'] == Status.objects.get(status='Not required'):
                issue_update.closed_date = timezone.now()
            issue_update.save()

        return HttpResponseRedirect(f'/issue/{issue_id}')

@login_required
def delete_comment(request, comment_id):
    '''Remove a comment associated with an issue'''
    comment = IssueComment.objects.get(id=comment_id)
    linked_issue = comment.issue_record
    comment.delete()
    return HttpResponseRedirect(f'/issue/{linked_issue.id}')

@login_required
def edit_comment(request, comment_id):
    data = {}
    comment_instance = IssueComment.objects.get(id=comment_id)
    edit_comment_form = AddCommentForm(instance=comment_instance, user=request.user)
    if request.method == 'POST':
        edit_comment_form = AddCommentForm(request.POST, user=request.user, instance=comment_instance)
        if edit_comment_form.is_valid():
            edit_comment_form.save()
            data['form_is_valid'] = True
        return redirect('issue_description', record_id=comment_instance.issue_record.id)
    context = {'edit_comment_form': edit_comment_form, 'comment_instance': comment_instance}
    html_form = render_to_string('helpdesk/modals/comment_modal.html', context, request=request)
    data['html_form'] = html_form
    return JsonResponse(data)


# TODO: Add in functionality to email bioinformatics when 1) a new issue is raised. 2) a non-binfx user adds a comment
# TODO: email issue owner when status is changed/ comment is made
# TODO: Add function for Bifx to change status, close issue