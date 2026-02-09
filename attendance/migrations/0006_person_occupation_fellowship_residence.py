# Generated manually for occupation, fellowship, residence fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0005_add_title_hierarchy"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="occupation",
            field=models.CharField(blank=True, max_length=100, default=""),
        ),
        migrations.AddField(
            model_name="person",
            name="fellowship",
            field=models.CharField(
                blank=True,
                choices=[
                    ("mens_fellowship", "Men's Fellowship"),
                    ("womens_fellowship", "Women's Fellowship"),
                    ("youth_fellowship", "Youth Fellowship"),
                    ("children", "Children"),
                    ("choir", "Choir"),
                    ("ushering", "Ushering"),
                    ("prayer", "Prayer"),
                    ("none", "None"),
                    ("other", "Other"),
                ],
                default="none",
                max_length=30,
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="residence",
            field=models.CharField(blank=True, max_length=200, default=""),
        ),
    ]
