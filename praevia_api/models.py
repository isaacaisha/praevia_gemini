# /home/siisi/praevia_gemini/praevia_api/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
import enum

# ───────────────────────────────────────────────────────────────
# ENUMS (unchanged)
# ───────────────────────────────────────────────────────────────
class AuditDecision(enum.Enum):
    CONTEST = 'CONTEST'
    DO_NOT_CONTEST = 'DO_NOT_CONTEST'
    NEED_MORE_INFO = 'NEED_MORE_INFO'
    REFER_TO_EXPERT = 'REFER_TO_EXPERT'
    @classmethod
    def choices(cls): return [(m.value, m.name) for m in cls]

class AuditStatus(enum.Enum):
    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    @classmethod
    def choices(cls): return [(m.value, m.name) for m in cls]

class ContentieuxStatus(enum.Enum):
    DRAFT = 'DRAFT'
    @classmethod
    def choices(cls): return [(m.value, m.name) for m in cls]

class JuridictionType(enum.Enum):
    TRIBUNAL_JUDICIAIRE = 'TRIBUNAL_JUDICIAIRE'
    COUR_APPEL          = 'COUR_APPEL'
    COUR_CASSATION      = 'COUR_CASSATION'
    @classmethod
    def choices(cls): return [(m.value, m.name) for m in cls]

class DocumentType(enum.Enum):
    DAT = 'DAT'
    CERTIFICAT_MEDICAL = 'CERTIFICAT_MEDICAL'
    ARRET_TRAVAIL = 'ARRET_TRAVAIL'
    TEMOIGNAGE = 'TEMOIGNAGE'
    DECISION_CPAM = 'DECISION_CPAM'
    EXPERTISE_MEDICALE = 'EXPERTISE_MEDICALE'
    LETTRE_RESERVE = 'LETTRE_RESERVE'
    CONTRAT_TRAVAIL = 'CONTRAT_TRAVAIL'
    FICHE_POSTE = 'FICHE_POSTE'
    RAPPORT_ENQUETE = 'RAPPORT_ENQUETE'
    NOTIFICATION_TAUX = 'NOTIFICATION_TAUX'
    COURRIER = 'COURRIER'
    AUTRE = 'AUTRE'
    @classmethod
    def choices(cls): return [(m.value, m.name) for m in cls]

class DossierStatus(enum.Enum):
    A_ANALYSER = 'A_ANALYSER'
    ANALYSE_EN_COURS = 'ANALYSE_EN_COURS'
    CONTESTATION_RECOMMANDEE = 'CONTESTATION_RECOMMANDEE'
    CONTESTATION_NON_RECOMMANDEE = 'CONTESTATION_NON_RECOMMANDEE'
    CLOTURE_SANS_SUITE = 'CLOTURE_SANS_SUITE'
    TRANSFORME_EN_CONTENTIEUX = 'TRANSFORME_EN_CONTENTIEUX'
    @classmethod
    def choices(cls): return [(m.value, m.name) for m in cls]

class UserRole:
    ADMIN = 'ADMIN'
    JURISTE = 'JURISTE'
    RH = 'RH'
    MANAGER = 'MANAGER'
    @staticmethod
    def choices():
        return [
            (UserRole.ADMIN,  'Admin'),
            (UserRole.JURISTE, 'Jurist'),
            (UserRole.RH,  'Rh'),
            (UserRole.MANAGER,  'Manager'),
        ]

# ───────────────────────────────────────────────────────────────
#  CUSTOM  USER  MODEL
# ───────────────────────────────────────────────────────────────
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email: raise ValueError("Email is required")
        email = self.normalize_email(email)
        user  = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)           # PBKDF2 hashing (Django default)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('role', UserRole.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name      = models.CharField(max_length=255)
    username  = models.CharField(max_length=255, unique=True)
    email     = models.EmailField(unique=True)
    role      = models.CharField(max_length=50, choices=UserRole.choices())
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    class Meta:
        db_table  = 'users'
        ordering  = ['-created_at']

    def __str__(self):
        return self.username

# ───────────────────────────────────────────────────────────────
#  OTHER MODELS  (only FK/M2M changed to settings.AUTH_USER_MODEL)
# ───────────────────────────────────────────────────────────────
class Action(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    class Meta:
        db_table  = 'actions'
        ordering  = ['-created_at']
    def __str__(self): return self.name

class Document(models.Model):
    contentieux   = models.ForeignKey('Contentieux', on_delete=models.CASCADE, related_name='documents_list')
    uploaded_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_documents')
    document_type = models.CharField(max_length=50, choices=DocumentType.choices())
    original_name = models.CharField(max_length=255)
    file          = models.FileField(upload_to='documents/', blank=True, null=True)
    mime_type     = models.CharField(max_length=100)
    size          = models.IntegerField()
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'documents'
        ordering = ['-created_at']
    def __str__(self): return self.original_name

class Contentieux(models.Model):
    dossier_atmp      = models.OneToOneField('DossierATMP', on_delete=models.CASCADE, related_name='contentieux_detail')
    reference         = models.CharField(max_length=255, unique=True)
    subject           = models.JSONField()
    status            = models.CharField(max_length=50, choices=ContentieuxStatus.choices())
    juridiction_steps = models.JSONField(default=dict)
    documents         = models.ManyToManyField(Document, related_name='contentieux_documents', blank=True)
    actions           = models.ManyToManyField(Action, related_name='contentieux_actions', blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'contentieux'
        ordering = ['-created_at']
    def __str__(self): return self.reference

class DossierATMP(models.Model):
    reference       = models.CharField(max_length=255, unique=True)
    status          = models.CharField(max_length=50, choices=DossierStatus.choices(), default=DossierStatus.A_ANALYSER.value)
    created_by      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_dossiers')
    entreprise      = models.JSONField()
    salarie         = models.JSONField()
    accident        = models.JSONField()
    temoins         = models.JSONField(default=list)
    tiers_implique  = models.JSONField(blank=True, null=True)
    service_sante   = models.CharField(max_length=255, blank=True, null=True)
    documents       = models.ManyToManyField(Document, related_name='dossier_atmp_documents', blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'dossiers_atmp'
        ordering = ['-created_at']
    def __str__(self): return self.reference

class Audit(models.Model):
    dossier_atmp = models.OneToOneField(DossierATMP, on_delete=models.CASCADE, related_name='audit_detail', unique=True)
    auditor      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audits_performed')
    status       = models.CharField(max_length=50, choices=AuditStatus.choices(), default=AuditStatus.NOT_STARTED.value)
    decision     = models.CharField(max_length=50, choices=AuditDecision.choices(), blank=True, null=True)
    comments     = models.TextField(blank=True, null=True)
    checklist    = models.JSONField(default=list)
    started_at   = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'audits'
        ordering = ['-created_at']
    def __str__(self): return f"Audit for {self.dossier_atmp.reference}"
