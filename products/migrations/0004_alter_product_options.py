# Generated by Django 3.2.13 on 2023-08-21 15:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_auto_20230813_1717"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ["id"],
                "verbose_name": "product",
                "verbose_name_plural": "products",
            },
        ),
    ]
