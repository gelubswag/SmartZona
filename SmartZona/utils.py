from django.db import models
from django.forms import ModelForm
from django.http.request import HttpRequest
from django.shortcuts import render


def model_crud(
    request: HttpRequest,
    form_model: ModelForm,
    model: models.Model,
    template: str,
    **kwargs
        ):
    form = form_model(request.POST or None)
    error: str | None = None
    if form.is_valid() and 'add' in request.POST:
        form.save()
    elif request.method == "GET":
        pass
    elif not form.is_valid() and 'add' in request.POST:
        error = "Ошибка при добавлении"
    elif request.POST.get('id') is None:
        error = "ID не может быть пустым"
    elif not request.POST.get('id').isdigit():
        error = "ID должен быть целым числом"
    elif 'change' in request.POST:
        obj = model.objects.filter(id=request.POST['id']).first()
        if obj:
            form = form_model(request.POST, instance=obj)
            if form.is_valid():
                form.save()
        else:
            error = "Ошибка при изменении"
    elif 'delete' in request.POST:
        obj = model.objects.filter(id=request.POST['id']).first()
        if obj:
            try:
                obj.delete()
            except:
                error = "Ошибка при удалении"
        else:
            error = "Ошибка при удалении"
    return render(
        request,
        template,
        {
            'objects': model.objects.all(),
            'form': form_model(),
            'error': error,
        } | kwargs
    )


def model_ctx(
    request: HttpRequest,
    form_model: ModelForm,
    model: models.Model,
    template: str,
    **kwargs
        ):
    form = form_model(request.POST or None)
    error: str | None = None
    if form.is_valid() and 'add' in request.POST:
        form.save()
    elif request.method == "GET":
        pass
    elif not form.is_valid() and 'add' in request.POST:
        error = "Ошибка при добавлении"
    elif request.POST.get('id') is None:
        error = "ID не может быть пустым"
    elif not request.POST.get('id').isdigit():
        error = "ID должен быть целым числом"
    elif 'change' in request.POST:
        obj = model.objects.filter(id=request.POST['id']).first()
        if obj:
            form = form_model(request.POST, instance=obj)
            if form.is_valid():
                form.save()
        else:
            error = "Ошибка при изменении"
    elif 'delete' in request.POST:
        obj = model.objects.filter(id=request.POST['id']).first()
        if obj:
            try:
                obj.delete()
            except:
                error = "Ошибка при удалении"
        else:
            error = "Ошибка при удалении"
    return {
        'request': request,
        'template_name': template,
        'context':
            {
                'objects': model.objects.all(),
                'form': form_model(),
                'error': error,
            } | kwargs
    }
