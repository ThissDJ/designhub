#from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render_to_response
from django.template import RequestContext
#from django.utils.translation import ugettext as _
#from livesettings import config_value
#from product.views import display_featured
#from satchmo_utils.views import bad_or_missing

#def home(request, template="shop/index.html"):
#    # Display the category, its child categories, and its products.
#    from localsite.models import Designer
#    designer  = Designer.objects.filter(featured=True, active=True)
##    from localsite.models import MyNewProduct
#    if designer.count > 0:
#        designer = designer[0]
##    mynewproducts = MyNewProduct
#    if request.method == "GET":
#        currpage = request.GET.get('page', 1)
#    else:
#        currpage = 1
#        
#    featured = display_featured()
#    
#    count = config_value('PRODUCT','NUM_PAGINATED')
#    
#    paginator = Paginator(featured, count)
#    
#    is_paged = False
#    page = None
#    
#    try:
#        paginator.validate_number(currpage)
#    except InvalidPage:
#        return bad_or_missing(request, _("Invalid page number"))
#            
#    is_paged = paginator.num_pages > 1
#    page = paginator.page(currpage)
#        
#    ctx = RequestContext(request, {
#        'all_products_list' : page.object_list,        
#        'is_paginated' : is_paged,
#        'page_obj' : page,
#        'paginator' : paginator,
#        'designer' : designer
#    })
#    
#    return render_to_response(template, context_instance=ctx)
#    modified by ljj 2012-10-3 for seprate the featured category
def home(request, template="shop/index.html"):
    # Display the category, its child categories, and its products.
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
    
    return render_to_response(template, context_instance=ctx)
    