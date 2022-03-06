from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.urls import reverse

from approval.models import Approval, APPROVAL_PENDING
from approval.models import approve_step, reject_step
from approval.forms import RejectionForm


def pending_approvals(request):
    qset = Approval.objects.filter(status=APPROVAL_PENDING, pending_on=request.user)
    #import pdb;pdb.set_trace()
    return render(request, "approval/list.html", {"approvals": qset})


def approval_detail(request, pk):
    approval = get_object_or_404(Approval, pk=pk)
    if request.method == "POST":
        #import pdb;pdb.set_trace()
        host_name = f'http://{request.get_host()}'
        approval_url = reverse('approval_detail', args=[pk])
        _url = f'{host_name}{approval_url}'
        if "approve" in request.POST:
            approve_step(approval, _url)
            return redirect("pending_approvals")
        else:
            return redirect("reject_approval", pk=pk)
    return render(request, "approval/detail.html", {"approval": approval})


def reject_approval(request, pk):
    approval = get_object_or_404(Approval, pk=pk)
    if request.method == "POST":
        form = RejectionForm(request.POST)
        if form.is_valid():
            reject_step(approval, form.cleaned_data["reason"])
            return redirect("pending_approvals")

    form = RejectionForm()
    return render(
        request, "approval/rejection.html", {"approval": approval, "form": form}
    )
