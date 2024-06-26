# Generated by Django 4.1.3 on 2024-03-15 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0011_rename_vote_source_attendee_source"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendee",
            name="source",
            field=models.CharField(
                choices=[("PLUS_ONE_COMMAND", "+1"), ("POLL_VOTE", "Poll Vote")],
                max_length=128,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="attendee",
            name="training",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attendees",
                to="bot.training",
            ),
        ),
    ]
