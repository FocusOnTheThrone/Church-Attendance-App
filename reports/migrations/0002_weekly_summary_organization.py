# Multi-tenancy: Add organization to WeeklySummary

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_organization_user_organization'),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeklysummary',
            name='organization',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='weekly_summaries',
                to='accounts.organization',
            ),
        ),
    ]
