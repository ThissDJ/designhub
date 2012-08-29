from django.views.generic import View, TemplateView, ListView, DetailView,\
                                CreateView, FormView
from plugshop.utils import load_class
from plugshop import settings
PRODUCT_CLASS = load_class(settings.PRODUCT_MODEL)
CATEGORY_CLASS = load_class(settings.CATEGORY_MODEL)

from django.shortcuts import get_object_or_404, redirect,render_to_response
from django.http import Http404,HttpResponse, HttpResponseRedirect
from django.utils import timezone
from testshop.shop.models import Designer, Category,Designer, ContactInfo, ContactInfoForm
from paypal.standard.forms import PayPalPaymentsForm
from django.core.urlresolvers import reverse
import testshop
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.messages.api import get_messages

from social_auth import __version__ as version
from social_auth.utils import setting
import json
def myimg(request):
    return HttpResponse('<img src="/media/img/img1.jpg"/>')

class ProductListViewHome(ListView):
    context_object_name = 'products'
    template_name = 'index.html'
    model = PRODUCT_CLASS

    def get_context_data(self, **kwargs):
        context = super(ProductListViewHome, self).get_context_data(**kwargs)
        categories = CATEGORY_CLASS.objects.all()
        designers = Designer.objects.all()
        contactInfoForm = ContactInfoForm()
        context.update(
            categories = categories,
            designers = designers,
            contactInfoForm = contactInfoForm,
        )
        context.update(
            sampleJpg = ['%s.jpg' %i for i in range(1,96)]
        )
        return context
def collectContactInfo(request):
    c = ContactInfo()
    f = ContactInfoForm(request.POST,instance = c)
    if f.is_valid():
        f.save()
        return HttpResponse('Thanks for joining us, our team will contact you soon.')
        #return redirect('/')
    else:
        return HttpResponse('Oh no! It seems you just input wrong infomation, plz try again.')
def myIndex(request):
    return HttpResponse('Hello Dude!')

class DesignerListView(ListView):
    context_object_name = 'designers'
    template_name = 'designer/designers.html'
    model = Designer

    def get_context_data(self, **kwargs):
        context = super(DesignerListView, self).get_context_data(**kwargs)
        designers = Designer.objects.all()
        categories = Category.objects.all()
        context.update(
            designers = designers ,
            categories = categories,
        )
        return context

class DesignerDetailView(DetailView):
    model = Designer
    template_name = 'designer/designer-details.html'
    def get_context_data(self, **kwargs):
        context = super(DesignerDetailView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        designers = Designer.objects.all()
        products = PRODUCT_CLASS.objects.filter(designer = context['object'])
        context.update(
            designers = designers ,
            categories = categories,
            products = products,
        )
        return context


def paypal(request):

    # What you want the button to do.

    paypal_dict = {
        "business": testshop.settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "0.01",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": "%s%s" % (testshop.settings.SITE_NAME, '/ipn-location/'),
        "return_url": "%s%s" % (testshop.settings.SITE_NAME, '/paypal/pdt/'),
        "cancel_return": "%s%s" % (testshop.settings.SITE_NAME, reverse('paypal-mycancel')),
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render_to_response("paypal.html", context)



from django.views.decorators.http import require_GET
from paypal.standard.pdt.models import PayPalPDT
from paypal.standard.pdt.forms import PayPalPDTForm
from django.core.mail import EmailMessage, mail_managers, \
                             mail_admins
from django.template.loader import render_to_string
from plugshop.cart import get_cart
from django.conf import settings as django_settings
def get_admin_mail_title(order):
    return settings.MESSAGE_NEW_ORDER_ADMIN

def get_customer_mail_title(order):
    return settings.MESSAGE_NEW_ORDER_USER

def notify_managers(request, order):
   
    cart = get_cart(request)
    from django.template.loader import render_to_string
    msg = render_to_string('plugshop/email/order_admin.html', {
        'cart': cart,
        'order': order,
        'total': cart.price_total(),
    })
    mail_managers(get_admin_mail_title(order), '', html_message=msg)
    
def notify_customer(request, order):    
    cart = get_cart(request)
    
    msg = render_to_string('plugshop/email/order_user.html', {
        'cart': cart,
        'order': order,
        'total': cart.price_total(),
    })
    mail = EmailMessage(get_customer_mail_title(order), msg, 
                        django_settings.SERVER_EMAIL, 
                        [order.user.email])
    mail.content_subtype = 'html'
    mail.send()


@require_GET
def pdt(request, item_check_callable=None, template="pdt/pdt.html", context=None):
    """Payment data transfer implementation: http://tinyurl.com/c9jjmw"""
    context = context or {}
    pdt_obj = None
    txn_id = request.GET.get('tx')
    failed = False
    if txn_id is not None:
        # If an existing transaction with the id tx exists: use it
        try:
            pdt_obj = PayPalPDT.objects.get(txn_id=txn_id)
        except PayPalPDT.DoesNotExist:
            # This is a new transaction so we continue processing PDT request
            pass
        
        if pdt_obj is None:
            form = PayPalPDTForm(request.GET)
            if form.is_valid():
                try:
                    pdt_obj = form.save(commit=False)
                except Exception, e:
                    error = repr(e)
                    failed = True
            else:
                error = form.errors
                failed = True
            
            if failed:
                pdt_obj = PayPalPDT()
                pdt_obj.set_flag("Invalid form. %s" % error)
            
            pdt_obj.initialize(request)
        
            if not failed:
                # The PDT object gets saved during verify
                pdt_obj.verify(item_check_callable)
    else:
        pass # we ignore any PDT requests that don't have a transaction id
 
    context.update({"failed":failed, "pdt_obj":pdt_obj})
    if pdt_obj.st == "SUCCESS":
        from plugshop.signals import order_create
        cart = get_cart(request)
        if len(cart) > 0:
            ORDER_FORM_CLASS = load_class(settings.ORDER_FORM)
            form = ORDER_FORM_CLASS({
                                     'name':'%s %s' %(pdt_obj.first_name, pdt_obj.last_name) \
                                     ,'email':pdt_obj.payer_email})
            form.is_valid()
    #        form.name = '%s %s' %(pdt_obj.first_name, pdt_obj.last_name)
    #        form.email = pdt_obj.payer_email
            order = form.save(cart=cart)
            
            notify_managers(request,order)
            notify_customer(request,order)
            
            from django.contrib import messages
            messages.info(request, settings.MESSAGE_SUCCESS)
            # delete storage
            from testshop.shop.models import Storage
            for cartItem in cart:
                s = Storage.objects.filter(product = cartItem.product,size = cartItem.size)
                if s > 0:
                    s = s[0]
                    s.num -= cartItem.quantity
                s.save()
            cart.empty()
            
            request.session['order'] = order
#        order_create.send(order=order, request=request)
        return render_to_response(template, context, RequestContext(request))
    else:
        return HttpResponse('paypal payment failed!')

@csrf_exempt
def ipnreturn(request):
    return HttpResponse(json.dumps(request.POST))
#    return HttpResponse('ipnreturn')


def ipncancel(request):
    return HttpResponse('ipncancel')

def profile(request):
    return redirect('/')



def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('social/home.html', {'version': version},
                                  RequestContext(request))


@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render_to_response('social/done.html', ctx, RequestContext(request))


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('social/error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


def form(request):
    if request.method == 'POST' and request.POST.get('username'):
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        request.session['saved_username'] = request.POST['username']
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('social/form.html', {}, RequestContext(request))


def form2(request):
    if request.method == 'POST' and request.POST.get('first_name'):
        request.session['saved_first_name'] = request.POST['first_name']
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('social/form2.html', {}, RequestContext(request))

def howDhubWorks(request):
    categories = CATEGORY_CLASS.objects.all()
    designers = Designer.objects.all()
    context={'categories':categories,\
             'designers':designers}
    return render_to_response('howworks.html', context, RequestContext(request))