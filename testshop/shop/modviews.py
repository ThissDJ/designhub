# encoding: utf-8
import testshop
from django.core.urlresolvers import reverse
from plugshop.views import *
from plugshop import settings
from plugshop.utils import load_class, serialize_model, serialize_queryset
from plugshop.forms import *
from plugshop.cart import get_cart
from paypal.standard.forms import PayPalPaymentsForm
from testshop.shop.models import Storage
from django.views.generic import CreateView
PRODUCT_CLASS = load_class(settings.PRODUCT_MODEL)
CATEGORY_CLASS = load_class(settings.CATEGORY_MODEL)
ORDER_CLASS = load_class(settings.ORDER_MODEL)
ORDER_PRODUCTS_CLASS = load_class(settings.ORDER_PRODUCTS_MODEL)

ORDER_FORM_CLASS = load_class(settings.ORDER_FORM)

from testshop.shop.models import Designer

class ProductListViewV1(ProductListView):
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        categories = CATEGORY_CLASS.objects.all()
        designers = Designer.objects.all()
        context.update(
            categories = categories,
            designers = designers,
        )
        return context

class ProductViewV1(ProductView):

    def get_context_data(self, *args, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        product = context.get('product')
        categories = CATEGORY_CLASS.objects.all()
        designers = Designer.objects.all()
#        storages = Storage.objects.filter(product = product, num__gte = 0)
        context.update(
            category=product.category,
            categories = categories,
            designers = designers,
#            storages = storages,
        )
        return context


class CategoryViewV1(CategoryView):
    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category = context.get('category')
        
        category_list = [category] + list(category.get_children())
        products = PRODUCT_CLASS.objects.filter(category__in=category_list)

        categories = CATEGORY_CLASS.objects.all()
        designers = Designer.objects.all()
        
        context.update(
            products = products,
            categories = categories,
            designers = designers,
        )
        return context

class CartViewV1(CartView):
    def get(self, request, **kwargs):
        cart = request.cart
        categories = CATEGORY_CLASS.objects.all()
        designers = Designer.objects.all()
        context = {}

        if request.is_ajax():
            context['cart'] = cart.serialize()
            return HttpResponse(json.dumps(context), 
                                content_type='application/json', **kwargs)
        else:
            context['form'] = ORDER_FORM_CLASS()
            if len(cart) == 0:
                return redirect('plugshop-product-list')
            else:
                context.update(
                    categories = categories,
                    designers = designers,
                )
                return self.render_to_response(context)
    
    def post(self, request, **kwargs):
        if request.is_ajax():
            action = request.POST.get('_action', None)
            cart = get_cart(request)
            
            if action == 'remove_all':
                cart.empty()
            else:
                form = ProductForm(request.POST)
    
                if form.is_valid():
                    product = form.cleaned_data.get('product')
                    quantity = form.cleaned_data.get('quantity', 1)
                    size = form.cleaned_data.get('size', None)
                    if action == 'add':
                        
                        result = {}
                        storages = product.checkStorage(size)
                        storageNum = 0
                        if len(storages) > 0:
                            for s in storages:
                                storageNum += s.num
                        if storageNum < int(quantity):
                            if size == None:
                                productName = product.name
                            else:
                                productName = product.name + ' (size: ' + size + ')'
                            result.update({'canBuy' : 'no','storage': storageNum \
                                           ,'productName':productName,'size':size})
                            return HttpResponse(json.dumps(result), 
                                               content_type='application/json', **kwargs)
                        else:       
                            cart.append(product, product.price, quantity=quantity,size=size)    
                    elif action == 'remove':
                        cart.remove(product, quantity=quantity,size=size)
    
                    elif action == 'remove_product':
                        cart.remove(product,size=size)    
                    else:
                        raise Http404
            cart.save()
            result = {}
            result.update({'canBuy': 'yes'
                           ,'redirectUrl': reverse('plugshop-cart')})
            return HttpResponse(json.dumps(result)#json.dumps(result), 
                                ,content_type='application/json', **kwargs)
        else:
            action = request.POST.get('_action', None)
            cart = get_cart(request)
            
            if action == 'remove_all':
                cart.empty()
            else:
                form = ProductForm(request.POST)
    
                if form.is_valid():
                    product = form.cleaned_data.get('product')
                    quantity = form.cleaned_data.get('quantity', 1)
                    size = form.cleaned_data.get('size', None)
                    
                    if action == 'add':
                        cart.append(product, product.price, quantity=quantity,size=size)
    
                    elif action == 'remove':
                        cart.remove(product, quantity=quantity,size=size)
    
                    elif action == 'remove_product':
                        cart.remove(product,size=size)
    
                    else:
                        raise Http404
            cart.save()
            if request.is_ajax():
                return HttpResponse(json.dumps({'cart': cart.serialize()}), 
                                    content_type='application/json', **kwargs)
            else:
                return redirect('plugshop-cart')

