from rest_framework.generics import (
    ListAPIView,
    CreateAPIView
)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Sale
from .serializers import (
    VentaReporteSerializer,
    ProcesoVentaSerializer,
    ProcesoVentaSerializer2,
)


class ReporteVentasList( ListAPIView ):
    serializer_class = VentaReporteSerializer

    def get_queryset(self):
        return Sale.objects.all()


class RegistrarVenta( CreateAPIView ):
    authentication_classes = ( TokenAuthentication, )
    permission_classes = [ IsAuthenticated ]
    serializer_class = ProcesoVentaSerializer

    def create( self, request, *args, **kwargs ):        
        serializer = self.serializer_class( data = request.data )
        serializer.is_valid( raise_exception = True )
        serializer.save( owner = request.user )
        
        return Response( { 'msj': 'Venta Exitosa' } )



class RegistrarVenta2( CreateAPIView ):
    authentication_classes = ( TokenAuthentication, )
    permission_classes = [ IsAuthenticated ]
    serializer_class = ProcesoVentaSerializer2

    def create( self, request, *args, **kwargs ):    
        serializer = self.serializer_class( data = request.data )
        serializer.is_valid( raise_exception = True )
        serializer.save( owner = request.user )
        
        return Response( { 'msj': 'Venta Exitosa' } )

