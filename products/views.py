from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Product

# Create your views here.

def home(request):
    return render(request, 'products/home.html')

@login_required
def create(request):
    if request.method == 'POST':
        post = request.POST
        title, url, image, icon, body = post.get('title'), post.get('url'), request.FILES.get('image'), \
                                        request.FILES.get('icon'), post.get('body')
        if all((title, url, image, icon, body)):
            product = Product()
            product.title = title
            product.body = body
            product.url = url
            product.icon = icon
            product.image = image
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            # TODO redirect to created product
            return redirect('home')
        else:
            return render(request, 'products/create.html', {'error':'All fields are required'})
    else:
        return render(request, 'products/create.html')