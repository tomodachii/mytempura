# Generated by Django 4.2.2 on 2023-07-31 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("nlp", "0003_entity_entity_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="entity",
            name="synonym",
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="entity",
            name="entity_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nlp.entitycategory",
                verbose_name="entity category",
            ),
        ),
        migrations.AlterField(
            model_name="response",
            name="response",
            field=models.CharField(verbose_name="response"),
        ),
        migrations.AlterField(
            model_name="trainingphrase",
            name="phrase",
            field=models.CharField(verbose_name="phrase"),
        ),
    ]
