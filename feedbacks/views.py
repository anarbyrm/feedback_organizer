from django.shortcuts import render
from django.http import JsonResponse

from .mongo_service import MongoService

mongo_service = MongoService()

def feedback_data_view(request):
    feedback_data = mongo_service.get_feedback_data()

    if not feedback_data:
        # if no data exists we proceed to seed data/feedback.json into db
        result = mongo_service.seed_feedback_data()
        if result:
            feedback_data = mongo_service.get_feedback_data()

    return JsonResponse({
        "feedbacks": feedback_data
    })

def branch_services_score_view(request):
    context = {}
    try:
        result = mongo_service.get_branch_services_scores_data()
        context.update({
            "success": True,
            "result": result
        })
    except Exception as exc:
        context.update({
            "success": False,
            "error_message": exc
        })

    return render(request, 'feedbacks/scores_table.html', context)
