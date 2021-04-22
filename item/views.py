from django.shortcuts import render, get_object_or_404, redirect
from .models import (
	Item,
	ItemImage,
)

# Create your views here.
def item(request, id):
	item = get_object_or_404(Item, id=id)
	itemImages = ItemImage.objects.filter(item=item)

	context = {
		'item' : item,
		'title' : item.title,
		'images' : itemImages
	}
	return render(request, 'item/item.html', context)