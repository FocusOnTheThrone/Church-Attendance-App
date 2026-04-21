# Backfill: Create default org and assign existing users/data to it

from django.db import migrations


def backfill_organization(apps, schema_editor):
    Organization = apps.get_model('accounts', 'Organization')
    User = apps.get_model('accounts', 'User')
    Person = apps.get_model('attendance', 'Person')
    Service = apps.get_model('attendance', 'Service')
    Fellowship = apps.get_model('attendance', 'Fellowship')
    WeeklySummary = apps.get_model('reports', 'WeeklySummary')

    # Create default org for existing data
    default_org, _ = Organization.objects.get_or_create(
        name='Default Church',
        defaults={}
    )

    # Assign users without org
    User.objects.filter(organization__isnull=True).update(organization=default_org)

    # Assign people, services, fellowships, weekly summaries
    Person.objects.filter(organization__isnull=True).update(organization=default_org)
    Service.objects.filter(organization__isnull=True).update(organization=default_org)
    Fellowship.objects.filter(organization__isnull=True).update(organization=default_org)
    WeeklySummary.objects.filter(organization__isnull=True).update(organization=default_org)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_organization_user_organization'),
        ('attendance', '0011_organization_multi_tenancy'),
        ('reports', '0002_weekly_summary_organization'),
    ]

    operations = [
        migrations.RunPython(backfill_organization, noop),
    ]
