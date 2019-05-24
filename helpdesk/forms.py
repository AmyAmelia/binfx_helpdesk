from datetime import datetime
from django import forms
from .models import *

class RaiseIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('issue','type','is_urgent','description')

