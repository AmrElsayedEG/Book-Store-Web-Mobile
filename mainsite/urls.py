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
from mainsite import views

app_name ='main'

urlpatterns = [
    path('', views.home,name='main_site_home'),
    #path('download/',views.download_ebooks,name='download_ebooks'),
    path('all/',views.all_books,name='all_books'),
    path('book/<slug:slug>/',views.one_book, name='book'),
    path('search/', views.search, name='search'),
    path('author/<int:id>/', views.get_author, name='author'),
    path('publisher/<int:id>/', views.get_publisher, name='publisher'),
    path('contact/', views.contact, name='contact-us'),
]
