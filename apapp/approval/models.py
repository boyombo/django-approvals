from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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

    def __str__(self):
        return str(self.model_name)


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
    field_name = models.CharField(max_length=100)
    field_type = models.PositiveIntegerField(choices=FIELD_TYPES, default=0)

    def __str__(self):
        return f'{self.initial_value} - {self.final_value}'


class ApprovalBase:

    def __init__(self, owner, obj):
        self.obj = obj
        self.owner = owner

        self.approval = self.save_approval()
        approvers = self.get_approvers()
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
            else:
                field_type = CHAR
                orig_val = getattr(original, fld.name)
                new_val = getattr(self.obj, fld.name)
            if orig_val != new_val:
                ApprovalChange.objects.create(
                    approval=self.approval,
                    initial_value=str(orig_val),
                    final_value=str(new_val),
                    field_name=fld.name,
                    field_type=field_type
                )

    def save_approval(self):
        app_label = self.obj._meta.app_label
        model_name = self.obj._meta.model_name
        model = f'{app_label}.{model_name}'
        return Approval.objects.create(
            initiator=self.owner,
            model_name=model,
            object_id=self.obj.pk
        )

