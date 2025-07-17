# /home/siisi/praevia_gemini/praevia_core/urls.py

from django.contrib import admin
from django.urls import path, include
from praevia_api import views # Import your app's views
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static
#from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

#def home_view(request):
#    return HttpResponse('🎉 Backend Praevia opérationnel!')
#
#def api_ok_view(request):
#    return JsonResponse({'message': 'API OK depuis /praevia'})

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', home_view),
    #path('api/', api_ok_view),
    
    # Custom API Root - now points to your custom APIRootView
    path('', views.RootAPIView.as_view(), name='api-root'),
    
    # Register the praevia_api app with a namespace
    path(
        'praevia/gemini/api/',
        include(('praevia_api.urls', 'praevia_api'), namespace='praevia_api')
    ),

    # Serve favicon.ico
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),

    # Optional: point root to custom view if needed
    #path('', include(('praevia_api.urls', 'praevia_api'))),  # optional
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
