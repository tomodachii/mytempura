# Generated by Django 4.2.2 on 2023-06-14 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("keywordrecognition", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="defaultmessage",
            name="bot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="default_messages",
                to="keywordrecognition.elizabot",
                verbose_name="bot",
            ),
        ),
    ]