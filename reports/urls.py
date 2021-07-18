"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from reports import views

app_name ='reports'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('orders/', views.orders,name='orders'),
    path('payments/', views.payment, name='payments'),
    path('visits/', views.visitors, name='visitors'),
    path('generate/<str:type>/', views.export_report, name="generate-report")
]
