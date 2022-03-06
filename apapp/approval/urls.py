from django.urls import path

from approval import views


urlpatterns = [
    path("pending/", views.pending_approvals, name="pending_approvals"),
    path("reject/<int:pk>/", views.reject_approval, name="reject_approval"),
    path(
        "detail/<int:pk>/", views.approval_detail, name="approval_detail"
    ),
]
