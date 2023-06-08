# Generated by Django 4.2.2 on 2023-06-08 10:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0002_alter_account_options_alter_account_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="email",
            field=models.CharField(
                blank=True, max_length=128, null=True, unique=True, verbose_name="email"
            ),
        ),
    ]