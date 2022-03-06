from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.apps import apps


APPROVAL_PENDING = 0
APPROVAL_APPROVED = 1
APPROVAL_REJECTED = 2
APPROVAL_STATUSES = enumerate(('Pending', 'Approved', 'Rejected'))

CHAR = 0
INT = 1
FLOAT = 2
FK = 3
FIELD_TYPES = enumerate(('Char', 'Int', 'Float', 'FK'))


class Approval(models.Model):
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(choices=APPROVAL_STATUSES, default=0)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    initiated = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200, blank=True)
    rejection_reason = models.TextField(blank=True)
    pending_on = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='approver')

    def __str__(self):
        return str(self.model_name)

    @property
    def current_step(self):
        steps = self.approvalstep_set.filter(status=APPROVAL_PENDING).order_by('step')
        try:
            return steps[0]
        except IndexError:
            return None


class ApprovalStep(models.Model):
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE)
    approver = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(choices=APPROVAL_STATUSES, default=0)
    step = models.PositiveIntegerField(default=1)
    last_step = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.approval} Step {self.step}'


class ApprovalChange(models.Model):
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE)
    initial_value = models.CharField(max_length=200)
    final_value = models.CharField(max_length=200)
    initial_text = models.CharField(max_length=200, blank=True)
    final_text = models.CharField(max_length=200, blank=True)
    field_name = models.CharField(max_length=100)
    field_type = models.PositiveIntegerField(choices=FIELD_TYPES, default=0)

    def __str__(self):
        return f'{self.initial_value} - {self.final_value}'


class EmailMessage(models.Model):
    PENDING = 'PENDING'
    SENT = 'SENT'
    ERROR = 'ERROR'
    EMAIL_STATUSES = ((PENDING, 'Pending'), (SENT, 'Sent'), (ERROR, 'Error'))

    sender = models.CharField(max_length=200)
    recipient = models.CharField(max_length=200)
    subject = models.CharField(max_length=50)
    body = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_sent = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=EMAIL_STATUSES)

    def __str__(self):
        return self.subject


class ApprovalBase:

    def __init__(self, owner, obj):
        self.obj = obj
        self.owner = owner

        approvers = self.get_approvers()
        first_approver = approvers[0]
        self.approval = self.save_approval(first_approver)
        for idx, approver in enumerate(approvers):
            is_last_step = True if idx + 1 == len(approvers) else False
            ApprovalStep.objects.create(
                approval=self.approval,
                approver=approver,
                status=APPROVAL_PENDING,
                step=idx+1,
                last_step=is_last_step
            )
        self.save_changes()

    def _is_fk(self, fld_name):
        try:
            fk = getattr(self.obj, f'{fld_name}_id')
        except AttributeError:
            return False
        return True

    def save_changes(self):
        #import pdb;pdb.set_trace()
        original = self.obj._meta.model.objects.get(pk=self.obj.pk)
        fields = [fld for fld in original._meta.fields if not fld.primary_key]
        for fld in fields:
            if self._is_fk(fld.name):
                field_type = FK
                orig_val = getattr(original, f'{fld.name}_id')
                new_val = getattr(self.obj, f'{fld.name}_id')
                orig_text = str(getattr(original, fld.name))
                new_text = str(getattr(self.obj, fld.name))
            else:
                field_type = CHAR
                orig_val = getattr(original, fld.name)
                new_val = getattr(self.obj, fld.name)
                orig_text = orig_val
                new_text = new_val
            if orig_val != new_val:
                ApprovalChange.objects.create(
                    approval=self.approval,
                    initial_value=str(orig_val),
                    final_value=str(new_val),
                    initial_text=orig_text,
                    final_text=new_text,
                    field_name=fld.name,
                    field_type=field_type
                )

    def save_approval(self, first_approver):
        app_label = self.obj._meta.app_label
        model_name = self.obj._meta.model_name
        model = f'{app_label}.{model_name}'
        description = f'{self.owner.username} edited {self.obj}'
        return Approval.objects.create(
            initiator=self.owner,
            model_name=model,
            object_id=self.obj.pk,
            description=description,
            pending_on=first_approver
        )


def approve_step(approval):
    step = approval.current_step
    if step:
        if not step.last_step:
            step.status = APPROVAL_APPROVED
            step.save()
            # current step has moved forward
            next_step = approval.current_step
            approval.pending_on = next_step.approver
            approval.save()
        else:
            # get object
            app_label, model_name = approval.model_name.split('.')
            model = apps.get_model(app_label, model_name)
            obj = model.objects.get(pk=approval.object_id)

            # apply changes
            for change in approval.approvalchange_set.all():
                if change.field_type == FK:
                    fld_name = f'{change.field_name}_id'
                else:
                    fld_name = change.field_name
                setattr(obj, fld_name, change.final_value)
            obj.save()
            approval.status = APPROVAL_APPROVED
            approval.save()
            step.status = APPROVAL_APPROVED
            step.save()


def reject_step(approval, reason):
    step = approval.current_step
    if step:
        step.status = APPROVAL_REJECTED
        step.save()
        approval.status = APPROVAL_REJECTED
        approval.rejected_reason = reason
        approval.save()
