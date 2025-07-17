# /home/siisi/praevia_gemini/praevia_api/management/commands/seed_data.py

import os
import sys
from pathlib import Path
from datetime import datetime
import bcrypt
from django.core.management.base import BaseCommand # Import BaseCommand
from django.utils import timezone # Import timezone for datetime objects

# No need for manual sys.path.append or django.setup() here,
# as Django's manage.py handles the environment setup for commands.

from praevia_api.models import ( # Use absolute import from praevia_api
    User, DossierATMP, DossierStatus, Document, DocumentType,
    Contentieux, ContentieuxStatus, Audit, AuditStatus, AuditDecision, Action
)

class Command(BaseCommand):
    help = 'Seeds the database with initial data for testing and development.'

    def handle(self, *args, **options):
        self.stdout.write("Starting data seeding...")

        # Clear existing data (optional, for clean slate)
        # Note: Deleting models with ForeignKeys will cascade deletions.
        # Delete in reverse order of dependency to avoid integrity errors if not using CASCADE
        Audit.objects.all().delete()
        Contentieux.objects.all().delete()
        DossierATMP.objects.all().delete()
        Document.objects.all().delete()
        User.objects.all().delete()
        Action.objects.all().delete()

        # Create Users
        # Use Django's built-in create_user method for proper password hashing
        admin_user = User.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='secret', # The password will be hashed by create_user
            name='Admin User',
            role='ADMIN',
            is_staff=True,      # Required for admin panel access
            is_superuser=True   # Required for superuser privileges
        )
        self.stdout.write(self.style.SUCCESS(f"Created user: {admin_user.username}"))

        juriste_user = User.objects.create_user(
            email='juriste@example.com',
            username='juriste',
            password='juriste123',
            name='Juriste Alpha',
            role='JURISTE'
        )
        self.stdout.write(self.style.SUCCESS(f"Created user: {juriste_user.username}"))

        rh_user = User.objects.create_user(
            email='rh@example.com',
            username='rh',
            password='rh123',
            name='RH Beta',
            role='RH'
        )
        self.stdout.write(self.style.SUCCESS(f"Created user: {rh_user.username}"))

        # Create a Dossier ATMP
        dossier_atmp_1 = DossierATMP(
            reference=f"DAT-{int(datetime.now().timestamp())}",
            status=DossierStatus.A_ANALYSER.value,
            created_by=rh_user, # Pass the User instance
            entreprise={
                'siret': '12345678900001',
                'raisonSociale': 'Entreprise Alpha',
                'adresse': '123 Rue de la Paix, Paris',
                'numeroRisque': '123AB'
            },
            salarie={
                'nom': 'Dupont',
                'prenom': 'Jean',
                'dateNaissance': datetime(1980, 5, 15).isoformat(), # Store as ISO format string for JSONField
                'numeroSecu': '180057512345678',
                'adresse': '456 Avenue des Champs, Paris',
                'horairesTravail': '9h-17h'
            },
            accident={
                'date': datetime(2024, 6, 1).isoformat(), # Store as ISO format string for JSONField
                'heure': '10:30',
                'lieu': 'Atelier',
                'circonstances': 'Chute d\'un objet lourd',
                'descriptionLesions': 'Fracture du pied droit'
            },
            temoins=[], # Empty list for JSONField
            tiers_implique=None, # None for JSONField
            service_sante='Service de Santé au Travail'
        )
        dossier_atmp_1.save()
        self.stdout.write(self.style.SUCCESS(f"Created Dossier ATMP: {dossier_atmp_1.reference}"))

        # Create a Contentieux (linked to dossier_atmp_1)
        contentieux_1 = Contentieux(
            dossier_atmp=dossier_atmp_1, # Link to the DossierATMP instance
            reference=f"CONT-{int(datetime.now().timestamp())}",
            subject={
                "title": f"Contentieux pour dossier {dossier_atmp_1.reference}",
                "description": f"Contentieux initié suite à l'audit du dossier AT/MP {dossier_atmp_1.reference}."
            },
            status=ContentieuxStatus.DRAFT.value,
            juridiction_steps={}
        )
        contentieux_1.save()
        self.stdout.write(self.style.SUCCESS(f"Created Contentieux: {contentieux_1.reference}"))

        # Create a Document (linked to contentieux_1)
        # For FileField, you'd typically use Django's FileSystemStorage or similar.
        # For seeding, we'll just create the model instance without an actual file for simplicity.
        # If you need actual files, you'd handle file creation and storage here.
        doc_1 = Document(
            contentieux=contentieux_1,
            uploaded_by=rh_user,
            document_type=DocumentType.DAT.value,
            original_name='DAT_Jean_Dupont.pdf',
            # file=None, # FileField can be null=True, blank=True
            mime_type='application/pdf',
            size=500000
        )
        doc_1.save()
        self.stdout.write(self.style.SUCCESS(f"Created Document: {doc_1.original_name}"))

        # Link document to contentieux (ManyToMany field)
        contentieux_1.documents.add(doc_1)
        contentieux_1.save()

        # Create an Audit for the dossier
        audit_1 = Audit(
            dossier_atmp=dossier_atmp_1, # Link to the DossierATMP instance
            auditor=juriste_user, # Link to the User instance
            status=AuditStatus.IN_PROGRESS.value,
            checklist=[], # Empty list for JSONField
            started_at=timezone.now()
        )
        audit_1.save()
        self.stdout.write(self.style.SUCCESS(f"Created Audit for Dossier: {dossier_atmp_1.reference}"))

        self.stdout.write(self.style.SUCCESS("Data seeding completed."))
