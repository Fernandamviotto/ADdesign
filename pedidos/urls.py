from django.urls import path
from .views import views_front, views_export, views_auth, views_dashboard

urlpatterns = [
    path('', views_dashboard.dashboard, name='dashboard'),  # /pedidos/
    path('login/', views_auth.login_view, name='login'),     # /pedidos/login/
    path('logout/', views_auth.logout_view, name='logout'),
    path('pedidos/criar/', views_front.criar_pedido, name='criar_pedido'),
    path('pedidos/<int:pk>/editar/', views_front.editar_pedido, name='editar_pedido'),
    path('pedidos/<int:pk>/', views_front.detalhes_pedido, name='detalhes_pedido'),
    path('exportar/pdf/', views_export.exportar_pdf, name='exportar_pdf'),
    path('exportar/excel/', views_export.exportar_excel, name='exportar_excel'),
]
