# Generated by Django 4.1.3 on 2024-03-15 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0010_remove_attendee_poll_attendee_training"),
    ]

    operations = [
        migrations.RenameField(
            model_name="attendee",
            old_name="vote_source",
            new_name="source",
        ),
    ]