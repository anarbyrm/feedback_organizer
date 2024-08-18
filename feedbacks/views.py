from django.shortcuts import render
from django.http import JsonResponse

from .mongo_service import MongoService

mongo_service = MongoService()

def feedback_list_view(request):
    feedbacks = mongo_service.get_all_feedbacks()
    return JsonResponse({
        "feedbacks": list(feedbacks)
    })

def organize_feedback_view(request):
    context = {}
    # todo: implement this view
    return render(request, 'feedback_table.html', context)
