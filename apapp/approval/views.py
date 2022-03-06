from django.shortcuts import render
from django.views.generic import ListView

from approval.models import Approval


class PendingApprovalsView(ListView):
    model = Approval
    template_name = 'approval/list.html'
