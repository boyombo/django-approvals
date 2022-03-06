from django.contrib import admin

from approval.models import Approval, ApprovalStep, ApprovalChange, EmailMessage


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "initiator",
        "status",
        "initiated",
        "model_name",
        "pending_on",
    ]


@admin.register(ApprovalStep)
class ApprovalStepAdmin(admin.ModelAdmin):
    list_display = ["approval", "approver", "status", "step", "last_step"]


@admin.register(ApprovalChange)
class ApprovalChangeAdmin(admin.ModelAdmin):
    list_display = [
        "approval",
        "initial_value",
        "final_value",
        "field_name",
        "field_type",
    ]


@admin.register(EmailMessage)
class EmailMessageAdmin(admin.ModelAdmin):
    list_display = [
        'sender',
        'recipient',
        'subject',
        'body',
        'date_created',
        'date_sent',
        'status'
    ]
