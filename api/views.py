from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse

from .utils import model_to_json, json_to_model, get_models

def test(request: HttpRequest):
    return JsonResponse({'test': 'OK'})


def get_all(request: HttpRequest, model_name: str):
    res_obj = model_to_json(model_name, True, request.GET.dict())
    if res_obj is None:
        return JsonResponse({'error': 'Model name was not found'})
    return JsonResponse(res_obj, safe=False)


def get_first(request: HttpRequest, model_name: str):
    res_obj = model_to_json(model_name, False, request.GET.dict())
    if res_obj is None:
        if model_name in get_models():
            return JsonResponse({'info': 'There are no models created'})
        return JsonResponse({'error': 'Model name was not found'})
    return JsonResponse(res_obj)


def post(request: HttpRequest, model_name: str):
    res_dict = json_to_model(model_name, request.GET.dict())
    return JsonResponse(res_dict)


def delete(request: HttpRequest, model_name: str, id: int):
    models = get_models()

    if model_name not in models:
        return JsonResponse({'error': 'Model name was not found'})
    
    model = models[model_name].objects.filter(id=id).first()

    if not model:
        return JsonResponse({'error': f"Didn't delete because model '{model_name}' of id '{id}' wasn't found"})

    model.delete()
    return JsonResponse({'OK': f'deleted {model_name} of id {id}'})