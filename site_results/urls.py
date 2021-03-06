from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.ResultsListView.as_view(), name='results'),
    path('products/', views.ProductsListView.as_view(), name='products'),
]
