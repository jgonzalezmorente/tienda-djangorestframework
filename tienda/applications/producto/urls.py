from django.urls import path
from . import views

app_name = 'producto_app'

urlpatterns = [
    path(
        'api/producto/por-usuario',
        views.ListProductUser.as_view(),
        name = 'product-producto-by_user'
    ),
    path(
        'api/producto/con-stok',
        views.ListProductStok.as_view(),
        name = 'product-producto-con_stok'
    ),
    path(
        'api/producto/por-genero/<gender>',
        views.ListProductGenero.as_view(),
        name = 'product-producto-por_genero'
    ),
    path(
        'api/producto/filtrar',
        views.FiltrarProductos.as_view(),
        name = 'product-filtrar'
    ),

]