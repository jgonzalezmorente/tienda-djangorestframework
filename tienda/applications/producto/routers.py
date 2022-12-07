from rest_framework.routers import DefaultRouter
from . import viewsets


router = DefaultRouter()
router.register( r'colors', viewsets.ColorViewset, basename = 'colors' )
router.register( r'productos', viewsets.ProductViewset, basename = 'productos' )

urlpatterns = router.urls
