from djangorestframework.resources import ModelResource
from testshop.shop.models import Comment

class CommentResource(ModelResource):
    model = Comment
    allowed_methods = ('GET','POST',)
    ordering = ('-created',)
    fields = ('id',('product',('id',)),('user',('username','id',)),'content','url','created',)
