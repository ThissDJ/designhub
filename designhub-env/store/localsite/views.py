from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
def example(request):
    ctx = RequestContext(request, {})
    return render_to_response('localsite/example.html', context_instance=ctx)

from social_auth import __version__ as version
from social_auth.utils import setting

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.messages.api import get_messages

from product.models import Discount
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

#designers
from django.views.generic import ListView, DetailView
from localsite.models import Designer
class DesignerListView(ListView):
    context_object_name = 'designers'
    template_name = 'designers/designers.html'
    model = Designer
    def get_context_data(self, **kwargs):
        context = super(DesignerListView, self).get_context_data(**kwargs)
        designers = Designer.objects.all().order_by('name')
        context.update(
            designers = designers ,
        )
        return context
class DesignerAjaxListView(ListView):
    context_object_name = 'talents'
    template_name = 'designers/designers-ajax.html'
    model = Designer
    def get_context_data(self, **kwargs):
        context = super(DesignerAjaxListView, self).get_context_data(**kwargs)
        designers = Designer.objects.filter(artist=False).order_by('name')
        artists = Designer.objects.filter(artist=True).order_by('name')
        talents = [list(designers),list(artists)]
        groupNum1 = 5.0
        groupNum2 = 2.0
        groupNums = [groupNum1,groupNum2]
        averagePersonNum1 =  len(designers) / groupNum1
        averagePersonNum2 =  len(artists) / groupNum2
        averagePersonNums = [averagePersonNum1, averagePersonNum2]
        talentGroups = [[],[]]
        for i_t in [0,1]:
            for i_d in range(0, len(talents[i_t])):
                d = talents[i_t][i_d]
                if len(talentGroups[i_t]) == 0:
                    talentGroups[i_t].append(['A-',[d]])
                else:
                    currentLetter = d.name[0:1].upper()
                    if talentGroups[i_t][-1][1][-1].name[0:1].upper() == currentLetter:
                        talentGroups[i_t][-1][1].append(d)
                    else:
                        if len(talentGroups[i_t][-1][1]) <= averagePersonNums[i_t] :
                            talentGroups[i_t][-1][1].append(d)
                        else :
                            talentGroups[i_t][-1][0] += talentGroups[i_t][-1][1][-1].name[0:1].upper()
                            talentGroups[i_t].append([d.name[0:1].upper() + '-',[d]])
            if talentGroups[i_t][-1][0].upper()[-1] == '-':
                 talentGroups[i_t][-1][0] += 'Z'
        class AZGroups:
            def __init__(self,name='',list=[]):
                self.name = name
                self.list = list
        designersList = []    
        for d in talentGroups[0]:
            azGroups = AZGroups(name=d[0] , list = d[1])
            designersList.append(azGroups)
        artistsList = []    
        for d in talentGroups[1]:
            azGroups = AZGroups(name=d[0] , list = d[1])
            artistsList.append(azGroups)
        context.update(
            designers = designersList ,
            artists = artistsList
        )
        return context
class DesignerDetailView(DetailView):
    model = Designer
    template_name = 'designers/designer-details.html'

from product.utils import find_best_auto_discount
from satchmo_store.shop.models import Cart
def saleindex(request):
    """
       display all the sale products
    """
    template = 'sale/index.html'
    discounts = Discount.objects.filter(active = True, automatic = True)
    products = []
    if discounts.count() > 0:
        for discount in list(discounts):
            if discount.valid_products.count() > 0:
                for product in discount.valid_products.filter(productvariation__parent__isnull=True).all():
                    product.discountIsValid, product.discountValidMsg = discount.isValid()
                    products.append(product)
    cart = Cart.objects.from_request(request)

    if cart.numItems > 0:
        productsInCart = [item.product for item in cart.cartitem_set.all()]
        sale = find_best_auto_discount(productsInCart)
    else:
        sale = None
       
    ctx = {
           'products':products,
           'sale': sale
           }
    return render_to_response(template, context_instance=RequestContext(request, ctx))

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def fabtabFeaturedToday(request):
    """
       facebook tab , featured today
    """
    from localsite.models import Designer
    from product.models import Category
    from product.models import Product
    designer  = Designer.objects.filter(featured=True, active=True)

    if designer.count > 0:
        designer = designer[0]

    featuredCatIds = [1,2,3]
    featuredCats = []
    for id in featuredCatIds:
        if len(Category.objects.filter(id=id)):
            featuredCats.append(Category.objects.get(id=id))
#    featured = display_featured()
    class FeaturedCat:
        def __init__(self,name='',list =[]):
            self.name = name
            self.list = list
    featuredCatsCls = []
    if len(featuredCats):
        for f in featuredCats:
            childCats = f.get_all_children()
            pList = []
            if len(childCats):
                for cc in childCats:
                    pListincc = Product.objects.filter(category = cc,featured = True, active = True)
                    if pListincc.count():
                        pList.extend(list(pListincc))
            if len(pList):
                fCls = FeaturedCat(name = f.name,list = pList)
                featuredCatsCls.append(fCls)
    from localsite.models import MyNewProduct
    featured_preorder_products_list = []
    featured_preorder_myNewProducts_list = MyNewProduct.objects.filter(preorder = True, featured = True)
    if featured_preorder_myNewProducts_list.count():
        for f in list(featured_preorder_myNewProducts_list):
            featured_preorder_products_list.append(f.product)
    ctx = RequestContext(request, {
        'featured_preorder_products_list' : featured_preorder_products_list,
        'featured_cats': featuredCatsCls,
        'designer' : designer
    })
    template = 'fbtab/featuredToday.html'
    return render_to_response(template, context_instance=RequestContext(request, ctx))

def launching(request):
    ctx = RequestContext(request, {
    })
    template = 'launching/subscription.html'
    if request.POST:
        from django.http import HttpResponse
        from django.core.mail import send_mail
        from django.conf import settings as email_settings
        subject = 'new talent'
        try: 
            message = request.POST['email']
            send_mail(subject, message, email_settings.DEFAULT_FROM_EMAIL, ['klijunjie@gmail.com','winston@designhub.hk'], auth_user= email_settings.EMAIL_HOST_USER,  auth_password= email_settings.EMAIL_HOST_PASSWORD)
            return HttpResponse(message)
        except:
            return HttpResponse('sucks')
    return render_to_response(template, context_instance=RequestContext(request, ctx))


from satchmo_store.contact.models import Contact
from satchmo_store.contact.forms import ExtendedContactInfoForm
from django.contrib.auth import REDIRECT_FIELD_NAME

from localsite.forms import ContactEmailPasswordForm
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from satchmo_store.contact import signals, CUSTOMER_ID
def createEmailPassword(request,
                    template_name='contact/create-email-password.html',
                    post_change_redirect=None,
                    create_email_password_form=ContactEmailPasswordForm,
                    current_app=None, extra_context=None):
    init_data = {}
    if post_change_redirect is None:
        post_change_redirect = reverse('django.contrib.auth.views.password_change_done')
    try:
        contact = Contact.objects.from_request(request, create=False)
    except Contact.DoesNotExist:
        contact = None
    if request.method == "POST":
        form = create_email_password_form(contact=contact, data=request.POST)
        if form.is_valid():
            if contact is None and request.user:
                contact = Contact(user=request.user)
            custID = form.save()
            request.session[CUSTOMER_ID] = custID
            redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = reverse('satchmo_account_info')

            return HttpResponseRedirect(redirect_to)
        else:
            signals.satchmo_contact_view.send(contact, contact=contact, contact_dict=init_data)
    else:
        signals.satchmo_contact_view.send(contact, contact=contact, contact_dict=init_data)
        form = create_email_password_form(contact=contact)
    context = {'form': form,}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

createEmailPassword = login_required(createEmailPassword)