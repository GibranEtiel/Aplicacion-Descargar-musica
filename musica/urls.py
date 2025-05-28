from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Descargarmusica/', include('Descargarmusica.urls')),
    path('', RedirectView.as_view(url='/Descargarmusica/', permanent=False)),  # Redirección a tu app
]
