from math import prod
from rest_framework import serializers
from .models import Sale, SaleDetail
        


class VentaReporteSerializer( serializers.ModelSerializer ):

    productos = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = (
            'id',
            'date_sale',
            'amount',
            'count',
            'type_invoce',
            'cancelado',
            'type_payment',
            'state',
            'adreese_send',
            'anulate',
            'user',
            'productos',
        )
    
    def get_productos( self, obj ):
        query = SaleDetail.objects.productos_por_venta( obj.id )
        productos_serializados = DetalleVentaProductoSerializer( query, many = True ).data
        return productos_serializados



class DetalleVentaProductoSerializer( serializers.ModelSerializer ):
    
    class Meta:
        fields = (
            'sale',
            'product',
            'count',
            'price_purchase',
            'price_sale',
            'anulate',
        )

        model = SaleDetail