# Generated by Django 4.1.3 on 2024-02-21 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0007_alter_pollvote_index_together"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pollvote",
            name="option",
        ),
        migrations.AddField(
            model_name="pollvote",
            name="go",
            field=models.BooleanField(default=False),
        ),
    ]