from django.urls import path

from approval import views


urlpatterns = [
    path('pending/', views.PendingApprovalsView.as_view(), name='pending_approvals'),
]
