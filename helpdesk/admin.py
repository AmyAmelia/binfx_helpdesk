from django.contrib import admin
from helpdesk import models

# Register your models here.
@admin.register(models.Issue)
class IssuesAdmin(admin.ModelAdmin):
   search_fields = ['issue']

admin.site.register(models.Status)
admin.site.register(models.RequestType)
admin.site.register(models.IssueComment)

