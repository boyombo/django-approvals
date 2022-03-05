from django.contrib.auth.models import User
from approval.models import ApprovalBase


class BookApproval(ApprovalBase):
    def __init__(self, owner, obj):
        super().__init__(owner, obj)

    def get_approvers(self):
        first = User.objects.get(username='approver1')
        second = User.objects.get(username='approver2')
        return [first, second]
