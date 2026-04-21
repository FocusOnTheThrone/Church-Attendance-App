# Add organizations M2M for multi-church switching

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_backfill_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='organizations',
            field=models.ManyToManyField(
                blank=True,
                help_text='Additional organizations this user can switch to.',
                related_name='members',
                to='accounts.organization',
            ),
        ),
    ]
