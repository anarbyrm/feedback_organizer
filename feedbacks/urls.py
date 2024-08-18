from django.urls import path

from .views import (feedback_list_view,
                    organize_feedback_view)

urlpatterns = [
    path('list/', feedback_list_view),
    path('organize/', organize_feedback_view),
]
