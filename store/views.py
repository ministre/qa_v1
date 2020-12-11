from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from store.models import Item
from .forms import ItemForm
from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.paginator import Paginator


@login_required
def item_full_list(request, page_id=1):
    items = Item.objects.all().order_by("-id")
    items_count = items.count()
    current_page_items = Paginator(items, 50)
    return render(request, 'store/item_full_list.html', {'items': current_page_items.page(page_id),
                                                         'items_count': items_count})


@login_required
def item_list(request, page_id=1):
    items = Item.objects.filter(returned_by=None).order_by("-id")
    items_count = items.count()
    current_page_items = Paginator(items, 50)
    return render(request, 'store/item_list.html', {'items': current_page_items.page(page_id),
                                                    'items_count': items_count})


@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            new_item = Item(name=request.POST['name'], location=request.POST['location'], comment=request.POST['comment'],
                            received_by=request.user)
            new_item.save()
            return HttpResponseRedirect('/store/')
    else:
        form = ItemForm()
        return render(request, 'store/item_create.html', {'form': form})


@login_required
def item_edit(request, item_id):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = Item.objects.get(id=item_id)
            item.name = request.POST['name']
            item.location = request.POST['location']
            item.comment = request.POST['comment']
            item.save()
            return HttpResponseRedirect('/store/')
    else:
        item = Item.objects.get(id=item_id)
        form = ItemForm(initial={'name': item.name, 'location': item.location, 'comment': item.comment})
        return render(request, 'store/item_edit.html', {'form': form, 'item': item})


@login_required
def item_return(request, item_id):
    item = Item.objects.get(id=item_id)
    item.location = ''
    item.returned_by = request.user
    item.date_of_returned = datetime.now()
    item.save()
    return HttpResponseRedirect('/store/')


@login_required
def item_search(request, page_id=1):
    if 'q' in request.GET:
        if request.GET['q'] == '':
            return HttpResponseRedirect('/store/')
        q = request.GET['q']
        items = Item.objects.filter(name__icontains=q)
        items_count = items.count()
        current_page_items = Paginator(items, 50)
        return render(request, 'store/item_search.html', {'items': current_page_items.page(page_id),
                                                          'items_count': items_count,
                                                          'q': q})

#        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'Отсутствует запрос!'
    return render(request, 'store/debug.html', {'message': message})
