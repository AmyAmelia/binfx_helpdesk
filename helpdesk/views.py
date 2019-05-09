from django.shortcuts import render, get_object_or_404

from django.utils import timezone
from .models import *


# Create your views here.

def raise_issue(request):
    return render(request, 'helpdesk/raise_issue.html')

def view_issues(request):
    ''' direct to view all submitted issues'''
    # posts = Issue.objects.filter(open_date__lte=timezone.now()).order_by('open_date')
    posts = Issue.objects.all()
    return render(request, 'helpdesk/view_issue.html',{'issues':posts})

def issue_description(request, pk):
    post = get_object_or_404(Issue, pk=pk)
    return render(request, 'helpdesk/issue_description.html', {'issue': post})



'''def variant(request):
    # collect all data
    patient = Patient.objects.all()

    # collect unique cancer types as a list and get counts for each
    types = [x.description for x in Description.objects.all()]
    type_counts = [len(patient.filter(id_description__description=t)) for t in types]
    # collect unique cancer stages as a list and get counts for each
    stages = [x.stage_str for x in Stage.objects.all()]
    stage_counts = [len(patient.filter(id_stage__stage_str=s)) for s in stages]

    stages = [stages[2], stages[0], stages[1]]
    stage_counts = [stage_counts[2], stage_counts[0], stage_counts[1]]
    stage_d = {'one':'1', 'two':'2', 'three':'3'}
    stages_num = [stage_d[x] for x in stages]

    # plots - type
    type_source = ColumnDataSource(data=dict(types=types, counts=type_counts))
    type_p = figure(x_range=types, plot_height=350, plot_width=520, toolbar_location=None, title="Number of variants per cancer type")
    type_p.vbar(x='types', top='counts', width=0.9, source=type_source,
           line_color='white', fill_color=factor_cmap('types', palette=['#5f27cd','#54a0ff','#00d2d3','#48dbfb','#ff6b6b','#1dd1a1','#feca57','#ff9ff3'], factors=types))
    type_p.xgrid.grid_line_color = None
    type_p.y_range.start = 0
    type_p.y_range.end = 1.1*max(type_counts)
    type_p.legend.orientation = "horizontal"
    type_p.legend.location = "top_center"
    type_p.xaxis.major_label_orientation = pi/4
    type_p.yaxis.axis_label='Frequency'
    type_script, type_div = components(type_p, CDN)

    # plots - stage
    stage_source = ColumnDataSource(data=dict(types=stages_num, counts=stage_counts))
    stage_p = figure(x_range=stages_num, plot_height=292, plot_width=320, toolbar_location=None, title="Number of variants per cancer stage")
    stage_p.vbar(x='types', top='counts', width=0.9, source=stage_source,
           line_color='white', fill_color=factor_cmap('types', palette=['#f1c40f','#e67e22','#e74c3c'], factors=stages_num))
    stage_p.xgrid.grid_line_color = None
    stage_p.y_range.start = 0
    stage_p.y_range.end = 1.1*max(stage_counts)
    stage_p.legend.orientation = "horizontal"
    stage_p.legend.location = "top_center"
    stage_p.xaxis.major_label_orientation = pi/4
    stage_p.yaxis.axis_label='Frequency'
    stage_script, stage_div = components(stage_p, CDN)

    return render(request, 'db/variant.html', {'patient': patient, 'type_counts': type_counts, 'stage_counts': stage_counts, 'type_script':type_script, 'type_div':type_div, 'stage_script':stage_script, 'stage_div':stage_div})
    #return render(request, 'db/variant.html', {'patient': patient, 'type_counts': type_counts, 'stage_counts': stage_counts})
'''