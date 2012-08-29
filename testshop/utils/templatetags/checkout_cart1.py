from django import template
register = template.Library()
import testshop
from django.core.urlresolvers import reverse
@register.filter
def checkout_cart1(value,arg=''):
    """checkout form."""
    pinput = []
    shortage = []
    if len(value.get_products()):
        for i,p in enumerate(value.get_products()):
            sizeExists = False
            if p.get('size'):
                sizeExists = True
            if sizeExists:
                storages = testshop.shop.models.Product.objects.get(id=p.get('product').get('id')).checkStorage(p.get('size'))
            else:
                storages = testshop.shop.models.Product.objects.get(id=p.get('product').get('id')).checkStorage()
            storageNum = 0
            if len(storages) > 0:
                for s in storages:
                    storageNum += s.num
            if storageNum < int(p.get('quantity')):
                if sizeExists:
                    productName = p.get('product').get('name') + ' (size: ' + p.get('size') + ')'
                else:
                    productName = p.get('product').get('name')    
                shortage.append([productName,storageNum])
            if p.get('size'):
                size = p.get('size')
                pinput.append(''.join(['<input type="hidden" name="amount_%i" value="%.1f">' %(i+1,p.get('price')) \
                                  ,' <input type="hidden" name="item_name_%i" value="%s">' %(i+1,p.get('product').get('name')) \
                                  ,'<input type="hidden" name="on0_%i" value="size">' %(i+1) \
                                  ,'<select style="display:none;" type="hidden" name="os0_%i">' %(i+1) \
                                  ,'<option type="hidden"  value="%s"  selected="selected">%s</option>' %(size,size) \
                                  ,'</select>' \
                                  ,'<input type="hidden" name="quantity_%i" value="%i">' %(i+1,p.get('quantity'))]))
            else:
                pinput.append(''.join(['<input type="hidden" name="amount_%i" value="%.1f">' %(i+1,p.get('price')) \
                                  ,' <input type="hidden" name="item_name_%i" value="%s">' %(i+1,p.get('product').get('name')) \
                                  ,'<input type="hidden" name="quantity_%i" value="%i">' %(i+1,p.get('quantity'))]))

    form_template =  ''.join(['<form action="https://www.sandbox.paypal.com/cgi-bin/webscr" method="post"> '
                             ,''.join(pinput)
        ,'<input type="hidden" name="upload" value="1"/>'
        ,'<input type="hidden" name="business" value="%s" id="id_business">' %testshop.settings.PAYPAL_RECEIVER_EMAIL
        ,'<input type="hidden" name="notify_url" value="%s%s" id="id_notify_url">' % (testshop.settings.SITE_NAME, reverse('paypal-ipn'))
        ,'<input type="hidden" name="cancel_return" value="%s%s" id="id_cancel_return">' % (testshop.settings.SITE_NAME, reverse('paypal-mycancel'))
        ,'<input type="hidden" name="return" value="%s%s" id="id_return_url">' % (testshop.settings.SITE_NAME, '/paypal/pdt/')
        ,'<input type="hidden" name="invoice" value="unique-invoice-id" id="id_invoice"><input type="hidden" name="cmd" value="_cart" id="id_cmd"><input type="hidden" name="charset" value="utf-8" id="id_charset"><input type="hidden" name="currency_code" value="HKD" id="id_currency_code"><input type="hidden" name="no_shipping" value="2" id="id_no_shipping"> \
    <input type="image" src="https://www.sandbox.paypal.com/en_US/i/btn/btn_buynowCC_LG.gif" border="0" name="submit" alt="Buy it Now"> \
</form>'])
    if len(shortage):
        return ''.join(['<h3>These are shortage of the following goods, plz decrease the quantity for ordering: </h3>' \
                        ,''.join(['<p>%s just has %i pieces</p>' %(s[0],s[1]) for s in shortage])])
    return form_template