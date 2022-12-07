from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .serializers import VentaReporteSerializer, ProcesoVentaSerializer2
from .models import Sale



class VentasViewSet( viewsets.ViewSet ):    
    authentication_classes = ( TokenAuthentication, )
    # permission_classes = [ IsAuthenticated ]    

    def get_permissions(self):
        if ( self.action == 'list' or self.action == 'retrieve' ):
            permission_classes = [ AllowAny ]
        else: 
            permission_classes = [ IsAuthenticated ]
        
        return [ permission() for permission in permission_classes ]
        

    def list( self, request ):
        queryset = Sale.objects.all()        
        serializer = VentaReporteSerializer( queryset, many = True )
        return Response( serializer.data )

    def create( self, request ):
        serializer = ProcesoVentaSerializer2( data = request.data )
        serializer.is_valid( raise_exception = True )
        serializer.save( owner = request.user )       
        return Response( { 'msj': 'Venta Exitosa' } )

    def retrieve( self, request, pk = None ):        
        venta = get_object_or_404( Sale.objects.all(), pk = pk )
        serializer = VentaReporteSerializer( venta )
        return Response( serializer.data )