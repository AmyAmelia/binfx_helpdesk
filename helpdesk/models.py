from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Issue(models.Model):
    '''Main table of the helpdesk, stores all issues and descriptions
    raised to the bioinformatics help desk'''
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='creator')
    type = models.ForeignKey('RequestType', on_delete=models.PROTECT,  null=True)
    issue = models.CharField(max_length=100, null=True)
    is_urgent = models.BooleanField(default = False)
    description = models.TextField(blank=True,null=True)
    status = models.ForeignKey('Status', on_delete=models.PROTECT,  null=True)
    open_date = models.DateTimeField(default=timezone.now)
    closed_date = models.DateTimeField(blank=True, null=True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='assignee', blank=True, null=True)
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='colab_issues', blank=True, null=True)

    class Meta:
        db_table = 'issue'
    def raise_issue(self):
        self.open_date = timezone.now()
        self.save()

    def __str__(self):
        return self.issue

class Status(models.Model):
    ''' Look up table for issue status '''
    status = models.CharField(max_length=20, null=True, unique=True)
    class Meta:
        db_table = 'status'
    def __str__(self):
        return self.status
    def __unicode__(self):
        return u'{0}'.format(self.status)

class RequestType(models.Model):
    ''' Look up table for the types of issue flag'''
    type = models.CharField(max_length=20, null=True, unique=True)
    class Meta:
        db_table = 'RequestType'
    def __str__(self):
        return self.type
    def __unicode__(self):
        return u'{0}'.format(self.type)

class IssueComment (models.Model):
    '''Model to record comments added to an issue. Permit multiple comments per issue '''
    issue_record = models.ForeignKey(Issue, on_delete=models.PROTECT,  null=True)
    comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    time = models.DateTimeField()

    class Meta:
        managed = True
        ordering = ['-time']
        db_table = 'IssueComment'
