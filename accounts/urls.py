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
from django.contrib.auth import views as auth_views

from . import views

from django.urls import reverse_lazy

app_name = 'accounts'

urlpatterns = [
    path('sign/', views.signpage, name='sign-user'),
    #path('myinfo/', views.profile_info),
    path('editinfo/', views.edit_profile, name='edit-personal'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('my-wishlist/', views.my_wish, name='my-wish-list'),
    path('wish-req-send/', views.wish_req, name='wish-req'),
    path('order/<int:id>/', views.one_order, name='one-order'),
    #Activate Email
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    #Change Password
    path('change-password/',views.change_password, name='change-pwd'),
    #Reset Password
    path('reset/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html",success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path('reset/password_reset/', views.password_reset_request, name="password_reset"),
    path('logout', views.logout_view, name='logout')
]
