from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
import json

from .utils import find_models_by_name, model_to_json, get_models

def test(request: HttpRequest):
    return JsonResponse({'test': 'OK'})


def get_all(request: HttpRequest, model_name: str):
    models = find_models_by_name(model_name, all=True, query_params=request.GET.dict())
    if not models:
        return JsonResponse({'error': 'Model name was not found'})

    res_obj = list()
    for model in models:
        res_obj.append(model_to_json(model))

    return JsonResponse(res_obj, safe=False)


def get_first(request: HttpRequest, model_name: str):
    model = find_models_by_name(model_name, all=False, query_params=request.GET.dict())
    if not model:
        return JsonResponse({'error': 'Model name was not found'})
    res_obj = model_to_json(model)
    return JsonResponse(res_obj)


def post(request: HttpRequest, model_name: str):
    models = get_models()

    if model_name not in models:
        return JsonResponse({'error': 'Model name was not found'})
    
    model_abstract = models[model_name]
    fields = { f.name:f for f in model_abstract._meta.get_fields() }

    if request.method == 'GET':
        data = request.GET.dict()
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({'error': f"Couldn't parse JSON"})
        
    kwargs = { k:v for k, v in data.items() if k in fields }

    fields_to_remove = []
    for k in kwargs:
        if isinstance(fields[k], DateTimeField):
            kwargs[k] = datetime.strptime(kwargs[k], '%Y-%m-%d_%H-%M-%S')
        elif isinstance(fields[k], ForeignKey):
            try:
                kwargs[k] = fields[k].related_model.objects.filter(id=kwargs[k]).first()
            except:
                fields_to_remove.append(k)
    print(kwargs)
    kwargs = { k:v for k, v in kwargs.items() if k not in fields_to_remove }

    try:
        model = model_abstract(**kwargs)
    except:
        return JsonResponse({'error': f"Couldn't create '{model_name}' with provided parameters\n\n{data}"})
    model.save()
    return HttpResponse('OK')


def delete(request: HttpRequest, model_name: str, id: int):
    models = get_models()

    if model_name not in models:
        return JsonResponse({'error': 'Model name was not found'})
    
    model = models[model_name].objects.filter(id=id).first()

    if not model:
        return JsonResponse({'error': f"Didn't delete because model '{model_name}' of id '{id}' wasn't found"})

    model.delete()
    return HttpResponse('OK')