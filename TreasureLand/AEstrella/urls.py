from django.urls import path

from . import views


app_name = "AEstrella"
urlpatterns = [
    path('grafo-json/', views.grafo_json, name='grafo-json'),
    path('grafo/', views.grafo, name='grafo'),
    path('grafo-json2/', views.ejecutar_astar, name='grafo-json2'),
    path('grafo2/', views.grafo2, name='grafo2'),
    #GRILLA
    path('grilla/', views.grilla_con_obstaculos, name='grilla'),
    #FUNCIONES DE GRILLA
    path('resolver-astar/', views.resolver_astar, name='resolver-astar'),
    path('guardar-grafo/', views.guardar_grafo, name='guardar_grafo'),
    path('listar-grafos/', views.obtener_grafos, name='listar_grafos'),
    path('cargar-grafo/<int:grafo_id>/', views.cargar_grafo, name='cargar_grafo'),
]
