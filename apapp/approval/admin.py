from django.contrib import admin

from approval.models import Approval, ApprovalStep, ApprovalChange


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ["initiator", "status", "model_name", "object_id"]


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
