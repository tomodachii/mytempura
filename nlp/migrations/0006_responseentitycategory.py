# Generated by Django 4.2.2 on 2023-08-01 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("nlp", "0005_alter_entity_entity_name_alter_entity_synonym"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResponseEntityCategory",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "required_category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="nlp.entitycategory",
                        verbose_name="required entity category",
                    ),
                ),
                (
                    "response",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="nlp.response",
                        verbose_name="response",
                    ),
                ),
            ],
            options={
                "verbose_name": "required entity category",
                "verbose_name_plural": "required entity category",
                "db_table": "nlp_response_entity_category",
                "ordering": ["response"],
            },
        ),
    ]