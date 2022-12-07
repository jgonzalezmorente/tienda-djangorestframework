from rest_framework import viewsets
from .models import Colors, Product
from .serializers import (
    ColorsSerializer, 
    ProductSerializerViewSet,
    PaginationSerializer
)


class ColorViewset( viewsets.ModelViewSet ):
    serializer_class = ColorsSerializer
    queryset = Colors.objects.all()


class ProductViewset( viewsets.ModelViewSet ):
    serializer_class = ProductSerializerViewSet
    queryset = Product.objects.all()
    pagination_class = PaginationSerializer

    def perform_create(self, serializer):
        serializer.save(
            video = 'https://www.youtube.com/@Neunapp'
        )

    def get_queryset(self):
        return Product.objects.productos_por_user( self.request.user )         
    

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)    
