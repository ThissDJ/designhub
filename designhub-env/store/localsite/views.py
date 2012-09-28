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
class DesignerDetailView(DetailView):
    model = Designer
    template_name = 'designers/designer-details.html'

def saleindex(request):
    """
       display all the sale products
    """
    template = 'sale/index.html'
    discounts = Discount.objects.filter(active = True)
    products = []
    if discounts.count() > 0:
        for discount in list(discounts):
            if discount.valid_products.count() > 0:
                for product in discount.valid_products.all():
                    products.append(product)
                
    ctx = {'products':products}
    return render_to_response(template, context_instance=RequestContext(request, ctx))