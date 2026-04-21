# Multi-tenancy: Add organization FK to Fellowship, Person, Service

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_organization_user_organization'),
        ('attendance', '0010_fellowship_alter_person_fellowship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fellowship',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='fellowship',
            name='organization',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='fellowships',
                to='accounts.organization',
            ),
        ),
        migrations.AddField(
            model_name='person',
            name='organization',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='people',
                to='accounts.organization',
            ),
        ),
        migrations.AddField(
            model_name='service',
            name='organization',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='services',
                to='accounts.organization',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='fellowship',
            unique_together={('organization', 'name')},
        ),
    ]
