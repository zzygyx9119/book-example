import json
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import List

User = get_user_model()


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    return render(request, 'list.html', {'list': list_, "form": form})


def list_items(request, list_id):
    list_ = List.objects.get(id=list_id)
    return HttpResponse(json.dumps(
        [{'id': item.id, 'text': item.text} for item in list_.item_set.all()]
    ), content_type='application/json')


def add_to_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_, data=request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse(json.dumps(dict(status="OK")), content_type="application/json")


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})

