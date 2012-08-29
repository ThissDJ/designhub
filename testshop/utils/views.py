from django.views.generic import CreateView, UpdateView, \
        DeleteView, ListView, DetailView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from testshop.shop.models import Product, Category, ProductImage, ProductUpdateForm, \
                           Designer,DesignerCreateForm

class DesignerCreateView(CreateView):
    """ 
    Sub-class of the CreateView to automatically pass the Request to the Form. 
    """
    success_message = "Created Successfully"
    model=Designer
    form_class=DesignerCreateForm
    template_name='admin-panel/add-designer.html'
    success_message='Designer adding successfully.'
    def get_success_url(self):
        return reverse('designer-detail',args=(self.object.slug,))

    def form_invalid(self, form):
        return http.HttpResponse("form is invalid.. this is just an HttpResponse object")
    def get_context_data(self, **kwargs):
        context = super(DesignerCreateView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        designers = Designer.objects.all()
        context.update(
            designers = designers ,
            categories = categories,
        )
        return context

class DesignerUpdateView(UpdateView):
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.        
    """
    model=Designer
    form_class=DesignerCreateForm
    template_name='admin-panel/update-designer.html'
    success_message='Designer updating successfully.'
    def get_success_url(self):
        return reverse('designer-detail',args=(self.object.slug,))
    def get_context_data(self, **kwargs):
        context = super(DesignerUpdateView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        designers = Designer.objects.all()
        context.update(
            designers = designers ,
            categories = categories,
        )
        return context

class DesignerDeleteView(DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other 
    user's data.
    """
    model = Designer
    template_name ='admin-panel/delete-designer.html'
    def get_success_url(self):
        return reverse("plugshop-designer-list")


class ProductUpdateView(UpdateView):
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.        
    """
    model=Product
    form_class=ProductUpdateForm
    template_name='admin-panel/update-product.html'
    success_message='Product updating successfully.'
    def get_success_url(self):
        #return reverse('designer-detail',args=(self.object.slug,))
        return self.object.get_absolute_url()
    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        designers = Designer.objects.all()
        context.update(
            designers = designers ,
            categories = categories,
        )
        return context