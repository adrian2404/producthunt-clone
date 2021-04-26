from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Vote

# Create your views here.

def home(request):
    user = request.user
    products_objects = Product.objects.all()
    products = []
    for product in products_objects:
        disable_vote = bool(Vote.objects.filter(product_id=product.id,
                                                user_id=user.id)) if user.is_authenticated else False
        products.append((product, disable_vote))
    return render(request, 'products/home.html', {'products': products})

@login_required(login_url="/accounts/signup")
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
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error':'All fields are required'})
    else:
        return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    disable_vote = bool(Vote.objects.filter(product_id=product_id, user_id=request.user.id)) if request.user.is_authenticated else False
    return render(request, 'products/detail.html',
                  {'product': product, 'disable_vote': disable_vote})

@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.save()
        vote = Vote(product_id=product.id, user_id=request.user.id)
        vote.save()
        return redirect('/products/' + str(product.id))
