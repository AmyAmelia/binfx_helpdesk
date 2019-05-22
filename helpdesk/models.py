from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Issue(models.Model):
    # id_issue = models.AutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.ForeignKey('RequestType', on_delete=models.CASCADE,  null=True)
    issue = models.CharField(max_length=100)
    description = models.TextField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE,  null=True)
    open_date = models.DateTimeField(default=timezone.now)
    closed_date = models.DateTimeField(blank=True, null=True)
    # TODO: add
    # TODO add stake-holders - many to many link required
    # TODO: look as Sisu- for how to restrict views per user group
    class Meta:
        db_table = 'issue'

    def raise_issue(self):
        self.open_date = timezone.now()
        self.save()

    def __str__(self):
        return self.issue

class Status(models.Model):
    # id_status = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, null=True, unique=True)
    class Meta:
        db_table = 'status'
    def __str__(self):
        return self.status
    def __unicode__(self):
        return u'{0}'.format(self.status)

class RequestType(models.Model):
    # id_type = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, null=True, unique=True)
    class Meta:
        db_table = 'RequestType'
    def __str__(self):
        return self.type
    def __unicode__(self):
        return u'{0}'.format(self.type)