# Generated by Django 5.0.2 on 2024-02-12 01:54

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
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
                ("sku", models.CharField(max_length=100)),
                ("name", models.CharField(max_length=255)),
                ("category", models.CharField(max_length=255)),
                ("tags", models.TextField()),
                ("stock_status", models.CharField(max_length=50)),
                ("available_stock", models.IntegerField()),
            ],
        ),
    ]