from django.utils import timezone
from rest_framework import serializers
from .models import Sale, SaleDetail
from applications.producto.models import Product        


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


class ProductDetailSerializer( serializers.Serializer ):    
    pk = serializers.IntegerField()
    count = serializers.IntegerField()


class ProcesoVentaSerializer( serializers.Serializer ):
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos = ProductDetailSerializer( many = True )

    def save( self, owner ):

        venta = Sale.objects.create(
            date_sale = timezone.now(),
            amount = 0,
            count = 0,
            type_invoce = self.validated_data['type_invoce'],
            type_payment = self.validated_data['type_payment'],
            adreese_send = self.validated_data['adreese_send'], 
            user = owner,
        )

        amount = 0
        count = 0

        productos = self.validated_data[ 'productos' ]

        ventas_detalle = []
        for producto in productos:
            prod = Product.objects.get( id = producto['pk'] )
            venta_detalle = SaleDetail(
                sale = venta,
                product = prod,
                count = producto['count'],
                price_purchase = prod.price_purchase,
                price_sale = prod.price_sale
            )

            amount += prod.price_sale * producto['count']
            count += producto['count']

            ventas_detalle.append( venta_detalle )

        venta.count = count
        venta.amount = amount
        venta.save()

        if ventas_detalle:
            SaleDetail.objects.bulk_create( ventas_detalle )


class ArrayIntegerSerializer( serializers.ListField ):
    child = serializers.IntegerField()


class ProcesoVentaSerializer2( serializers.Serializer ):
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos = ArrayIntegerSerializer()
    cantidades = ArrayIntegerSerializer()

    def validate( self, data ):
        if data['type_payment'] != '0':
            raise serializers.ValidationError( 'Ingrese un tipo de pago correcto' )
        return data

    def validate_type_invoce( self, value ):
        if value != '0':
            raise serializers.ValidationError( 'Ingrese un valor correcto' )
        
        return value

    
    def save( self, owner ):
        venta = Sale.objects.create(
            date_sale = timezone.now(),
            amount = 0,
            count = 0,
            type_invoce = self.validated_data['type_invoce'],
            type_payment = self.validated_data['type_payment'],
            adreese_send = self.validated_data['adreese_send'], 
            user = owner,
        )

        amount = 0
        count = 0

        productos = Product.objects.filter(
            id__in = self.validated_data[ 'productos' ]
        )

        cantidades = self.validated_data[ 'cantidades' ]

        ventas_detalle = []
        for producto, cantidad in zip( productos, cantidades ):
            venta_detalle = SaleDetail(
                sale = venta,
                product = producto,
                count = cantidad,
                price_purchase = producto.price_purchase,
                price_sale = producto.price_sale
            )

            amount += producto.price_sale * cantidad
            count += cantidad
            ventas_detalle.append( venta_detalle )

        venta.count = count
        venta.amount = amount
        venta.save()

        if ventas_detalle:
            SaleDetail.objects.bulk_create( ventas_detalle )
