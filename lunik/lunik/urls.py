"""testDjango URL Configuration

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
from django.contrib import admin

from django.urls import path,include,reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    #path('',RedirectView.as_view(url=reverse_lazy('authorization:dashboard'))),
    path('panel/', include(('panel.authorization.urls','authorization'), namespace='authorization')),
    #-- Accounts
    path('panel/accounts/', include(('panel.accounts.urls','accounts'), namespace='accounts')),
    #-- Config panel
    path('panel/config/', include(('panel.config.urls','config'), namespace='config')),
    #-- Sessions
    path('panel/config/', include(('user_sessions.urls','user_sessions'), namespace='user_sessions')),
    #-- Products
    path('panel/products/', include(('panel.products.urls', 'products'), namespace='products')),
    #-- Shopping orders
    path('panel/orders/', include(('panel.orders.urls','orders'), namespace='orders')),
    #-- Webiste
    path('panel/website/', include(('panel.website.urls', 'website'), namespace='website')),
    #-- Recovery Password
    path('recovery/', include('django.contrib.auth.urls')),
    #-- Summernote texteditor
    path('summernote/', include('django_summernote.urls')),

    #-- Shop urls

    path('', include(('portal.shop.urls','shop'), namespace='shop_cart')),

]
#-- Static files * ONLY IN DEVELOP *
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
