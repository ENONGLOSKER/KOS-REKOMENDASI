"""
URL configuration for rekomendasiKOS_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rekomendasiKOS_app import views

# STATIC
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # dashboard
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/kos/',views.dashboard_kos,name='dsb_kos'),
    path('dashboard/kos/add/',views.dashboard_kos_add,name='dsb_add_kos'),
    path('dashboard/kos/update/<int:id>/',views.dashboard_kos_edit,name='dsb_edit_kos'),
    path('dashboard/kos/delete/<int:id>/',views.dashboard_kos_delete,name='dsb_delete_kos'),
    path('dashboard/pesanan/',views.dashboard_pesanan,name='dsb_pesanan'),

    # home
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('status/',views.status,name='status'),
    path('detail/<int:id>/',views.detail,name='detail'),
    path('buat_pesanan/<int:id>/',views.buat_pesanan,name='buat_pesanan'),
    
    path('singin/',views.signin_user,name='signin'),
    path('signup/',views.signup_user,name='signup'),
    path('signout/',views.signout_user,name='signout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)