from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie import fields
from .models import Data
from django.contrib.auth.models import User
from django.db.models import Q


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth_user'
        fields = ['username']


class DataResource(ModelResource):

    created_by = fields.ForeignKey(UserResource, 'created_by', null=True, blank=True, full=True)

    class Meta:
        queryset = Data.objects.all()
        allowed_methods = ['get']
        resource_name = 'data'
        filtering = {
            'title': ALL,
            'description': ['icontains'],
            'code': ['icontains'],
            'project': ['icontains']
        }


    def build_filters(self, filters=None, **kwargs):
        if filters is None:
            filters = {}
        orm_filters = super(DataResource, self).build_filters(filters, **kwargs)

        if ('query' in filters):
            query = filters['query']
            qset = (
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(code__icontains=query) |
                    Q(project__icontains=query) |
                    Q(tags__icontains=query)
            )
            orm_filters.update({'custom': qset})

        return orm_filters

    def apply_filters(self, request, applicable_filters):
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None

        semi_filtered = super(DataResource, self).apply_filters(request, applicable_filters)

        return semi_filtered.filter(custom) if custom else semi_filtered

    # def get_object_list(self, request):
    #     return super(DataResource, self).get_object_list(request).filter(start_date__gte=datetime.datetime.now)

        # def apply_filters(self, request, applicable_filters):
        #     base_object_list = super(DataResource, self).apply_filters(request, applicable_filters)
        #     query = request.GET.get('query', None)
        #     print(query)
        #     filters = {}
        #     if query:
        #         qset = (
        #                 Q(title__icontains=query, **filters) |
        #                 Q(description__icontains=query, **filters)
        #         )
        #         base_object_list = base_object_list.filter(qset)
        #     return base_object_list.filter(**filters).distinct()
