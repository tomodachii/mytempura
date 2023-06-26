# Generated by Django 4.2.2 on 2023-06-22 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0004_bot"),
        ("keywordrecognition", "0002_alter_defaultmessage_bot"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="elizabot",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="elizabot",
            name="description",
        ),
        migrations.RemoveField(
            model_name="elizabot",
            name="id",
        ),
        migrations.RemoveField(
            model_name="elizabot",
            name="name",
        ),
        migrations.RemoveField(
            model_name="elizabot",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="elizabot",
            name="updated_at",
        ),
        migrations.AddField(
            model_name="elizabot",
            name="bot_ptr",
            field=models.OneToOneField(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="backend.bot",
            ),
        ),
        migrations.DeleteModel(
            name="Quit",
        ),
    ]