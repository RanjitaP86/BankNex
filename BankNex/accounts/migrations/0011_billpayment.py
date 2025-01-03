# Generated by Django 5.1.2 on 2024-12-27 06:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_remove_transaction_description"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BillPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bill_category", models.CharField(max_length=255)),
                ("bill_provider", models.CharField(max_length=255)),
                ("bill_number", models.CharField(max_length=255)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("due_date", models.DateField()),
                ("payment_date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("Pending", "Pending"), ("Completed", "Completed")],
                        default="Pending",
                        max_length=10,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
