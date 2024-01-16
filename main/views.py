from typing import Any
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from user.models import Profile





def home(request: HttpRequest):
    # if request.user.is_authenticated:
    #     if request.user.profile.position_type == Profile.PositionType.DRIVER:
    #         return render(request, 'main/driver_home.html')
    return render(request, 'main/home.html')



### api

# from main.utils import get_all_nonabstract_models_from_module
# api_models = get_all_nonabstract_models_from_module('main.models') | get_all_nonabstract_models_from_module('user.models')

# @login_required
# @require_http_methods(['GET', 'DELETE'])
# def api_single(request: HttpRequest, url_name: str, model_id: id):
#     if request.user.profile.position_type < 3:
#         return HttpResponseForbidden("You haven't got the rank to view this page")
#     if url_name not in api_models:
#         return HttpResponseNotFound('This url does not match to any api path')
#     model_class = api_models[url_name]
#     if not model_class.objects.filter(id=model_id).exists():
#         return HttpResponseNotFound(f'No model instance of "{url_name}" with id "{model_id}" found')
#     model_instance = model_class.objects.get(id=model_id)
#     if request.method == 'GET':
#         return JsonResponse({'id': model_instance.id, 'str': str(model_instance)})
#     elif request.method == 'DELETE':
#         model_instance.delete()
#         return JsonResponse({'status': 'OK', 'message': 'deleted model instance'})
#     elif request.method == 'POST': # TODO: needs type checking!!!
#         for qp_key, qp_value in request.GET.items():
#             if not hasattr(model_instance, qp_key):
#                 return HttpResponseBadRequest(f'Model instance of "{url_name}" has no attribute named "{qp_key}"')
#             setattr(model_instance, qp_key, qp_value)
#         model_instance.save()
#         return JsonResponse({'status': 'OK', 'message': 'saved changes'})
#     return HttpResponseServerError(f'The method "{request.method}" is not supported in this path')

# @login_required
# @require_http_methods(['GET'])
# def api_multiple(request: HttpRequest, url_name: str):
#     if request.user.profile.position_type < 3:
#         return HttpResponseForbidden("You haven't got the rank to view this page")
#     if url_name not in api_models:
#         return HttpResponseNotFound('This url does not match to any api path')
#     model_class = api_models[url_name]
#     if request.method == 'GET':
#         model_instances = model_class.objects.all()
#         return JsonResponse([{'id': m.id, 'str': str(m)} for m in model_instances], safe=False)
#     elif request.method == 'PUT':
#         try:
#             new_model = model_class(**{k:v for k, v in request.GET.items()})
#             new_model.save()
#             return JsonResponse({'status': 'OK', 'message': 'created instance', 'id': new_model.id})
#         except Exception as err:
#             return HttpResponseBadRequest(str(err))
#     return HttpResponseServerError(f'The method "{request.method}" is not supported in this path')


### utils views

def hello_world(request: HttpRequest):
    return HttpResponse('Hello, world!')


def test(request:HttpRequest):
    context = {
        'user_info': True
    }
    return render(request, 'main/test.html', context=context)
