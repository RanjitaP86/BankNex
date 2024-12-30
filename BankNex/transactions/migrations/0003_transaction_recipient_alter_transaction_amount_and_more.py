# Generated by Django 5.1.2 on 2024-12-26 16:39

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0002_rename_timestamp_transaction_date_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="recipient",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="description",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="transactions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
