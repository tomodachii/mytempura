# Generated by Django 4.2.2 on 2023-07-30 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("nlp", "0002_entity_intent_response_trainingphrase_responseentity_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="entity",
            name="entity_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nlp.entitycategory",
                verbose_name="nlp bot",
            ),
        ),
    ]
