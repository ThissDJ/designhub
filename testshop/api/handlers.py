from djangorestframework.mixins import PaginatorMixin,InstanceMixin,ReadModelMixin
from djangorestframework.renderers import DEFAULT_RENDERERS
from djangorestframework.views import ListOrCreateModelView,ListModelView,ModelView
from djangorestframework.response import Response, ErrorResponse
from djangorestframework import status
from django.core.paginator import Paginator


class PaginatorListOrCreateModelView(PaginatorMixin, ListOrCreateModelView):
    """An example view using Django 1.3's class based views.
    Uses djangorestframework's RendererMixin to provide support for multiple output formats."""
    renderers = DEFAULT_RENDERERS

class AutoOwnerPaginatorListOrCreateModelView(PaginatorListOrCreateModelView):
    def post(self, request, *args, **kwargs):
        model = self.resource.model

        # Copy the dict to keep self.CONTENT intact
        content = dict(self.CONTENT)
        m2m_data = {}
        content.update({'user':request.user})
        for field in model._meta.many_to_many:
            if field.name in content:
                m2m_data[field.name] = (
                    field.m2m_reverse_field_name(), content[field.name]
                )
                del content[field.name]
        
        instance = model(**self.get_instance_data(model, content, *args, **kwargs))
        instance.save()
        
        for fieldname in m2m_data:
            manager = getattr(instance, fieldname)
        
            if hasattr(manager, 'add'):
                manager.add(*m2m_data[fieldname][1])
            else:
                data = {}
                data[manager.source_field_name] = instance
                
                for related_item in m2m_data[fieldname][1]:
                    data[m2m_data[fieldname][0]] = related_item
                    manager.through(**data).save()
        
        headers = {}
        if hasattr(instance, 'get_absolute_url'):
            headers['Location'] = self.resource(self).url(instance)
        return Response(status.HTTP_201_CREATED, instance, headers)

class ReadOnlyInstanceModelView(InstanceMixin, ReadModelMixin, ModelView):
    """
    A view which provides default operations for read/ against a model instance.
    """
    _suffix = 'Instance'
