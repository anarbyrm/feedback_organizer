from django.urls import path

from .views import (feedback_data_view,
                    branch_services_score_view)

urlpatterns = [
    path('', feedback_data_view),
    path('scores/', branch_services_score_view),
]
