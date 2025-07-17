# /home/siisi/praevia_gemini/praevia_api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomAPIRootView,
    AuditByDossierIdView,
    AuditFinalizeView,
    get_jurist_dashboard_data,
    get_rh_dashboard_data,
    get_qse_dashboard_data,
    get_direction_dashboard_data,
    DocumentUploadView,
    DocumentDownloadView,
    DossierATMPViewSet,
    ContentieuxViewSet,
    AuditViewSet,
    DocumentViewSet
)
from .auth_views import UserViewSet, LoginView, LogoutView

app_name = 'praevia_api'

router = DefaultRouter()
# Register ViewSets with the router
router.register(r'users', UserViewSet, basename='user')
router.register(r'dossiers', DossierATMPViewSet, basename='dossier')
router.register(r'contentieux', ContentieuxViewSet, basename='contentieux')
router.register(r'audits', AuditViewSet, basename='audit')
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    # API root
    path('', CustomAPIRootView.as_view(), name='root_api'),
    
    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Dashboard endpoints
    path('dashboard/juridique/', get_jurist_dashboard_data, name='jurist_dashboard_data'),
    path('dashboard/rh/', get_rh_dashboard_data, name='rh_dashboard_data'),
    path('dashboard/qse/', get_qse_dashboard_data, name='qse_dashboard_data'),
    path('dashboard/direction/', get_direction_dashboard_data, name='direction_dashboard_data'),

    # Special case endpoints
    path('dossiers/<int:dossier_id>/audit/', AuditByDossierIdView.as_view(), name='audit-by-dossier'),
    path('audits/<int:audit_id>/finalize/', AuditFinalizeView.as_view(), name='finalize-audit'),
    path('documents/upload/', DocumentUploadView.as_view(), name='upload_document'),
    path('documents/<int:document_id>/download/', DocumentDownloadView.as_view(), name='download_document'),
    
    # Include router URLs
    path('', include(router.urls)),
]
