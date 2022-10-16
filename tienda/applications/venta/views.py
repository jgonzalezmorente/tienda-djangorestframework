from rest_framework.generics import (
    ListAPIView
)
from .models import Sale
from .serializers import VentaReporteSerializer


class ReporteVentasList( ListAPIView ):
    serializer_class = VentaReporteSerializer

    def get_queryset(self):
        return Sale.objects.all()