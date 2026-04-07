from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse


class HATEOASPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'results': data,
            '_links': self._build_links(),
            '_meta': {
                'page': self.page.number,
                'pages': self.page.paginator.num_pages,
                'page_size': len(data),
            }
        })
    
    def _build_links(self):
        base_url = self.request.build_absolute_uri().split('?')[0]
        query_params = self.request.GET.copy()
        
        links = {
            'self': self.request.build_absolute_uri(),
        }
        
        if self.page.has_next():
            query_params['page'] = self.page.next_page_number()
            links['next'] = f"{base_url}?{query_params.urlencode()}"
        
        if self.page.has_previous():
            query_params['page'] = self.page.previous_page_number()
            links['previous'] = f"{base_url}?{query_params.urlencode()}"
        
        query_params['page'] = 1
        links['first'] = f"{base_url}?{query_params.urlencode()}"
        
        query_params['page'] = self.page.paginator.num_pages
        links['last'] = f"{base_url}?{query_params.urlencode()}"
        
        return links