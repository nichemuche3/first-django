from django.shortcuts import render, redirect
from .models import Phone

def index(request):
    return redirect('catalog')

def show_catalog(request):
    template = 'catalog.html'
    
    sort = request.GET.get('sort', '')
    
    phones = Phone.objects.all()
    
    if sort == 'name':
        phones = phones.order_by('name')
    elif sort == 'min_price':
        phones = phones.order_by('price')
    elif sort == 'max_price':
        phones = phones.order_by('-price')
    
    context = {
        'phones': phones
    }
    return render(request, template, context)

def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    
    context = {
        'phone': phone
    }
    return render(request, template, context)