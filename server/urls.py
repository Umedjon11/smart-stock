from django.contrib import admin
from django.urls import path, include
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
    path('', include('transfers.urls')),
    path('', include('accounts.urls')),
    path('', include('reports.urls')),
    path('', include('suppliers.urls')),
    path('products/',include('products.urls')),
    path('warehouses/', include('warehouses.urls')),
    path('', include('base.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)