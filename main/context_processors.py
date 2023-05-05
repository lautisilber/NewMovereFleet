from django.http import HttpRequest
from typing import Any

from .models import Vehicle, Company, QuestionType


def load_navbar_context(request: HttpRequest) -> dict[str, Any]:
    context = {}
    if request.user.is_authenticated:
        if request.user.profile.position_type == 1 or request.user.profile.position_type == 2:
            context = {
                'base_vehicles': sorted(list(set(Vehicle.objects.filter(questiontemplate__position_type=request.user.profile.position_type).all())), key=lambda v: v.id) # TODO: make this more efficient
            }
        elif request.user.profile.position_type >= 3:
            context = {
                'base_vehicles': Vehicle.objects.all(),
                'base_companies': Company.objects.all(),
                'base_question_types': QuestionType.objects.all()
            }
    return context