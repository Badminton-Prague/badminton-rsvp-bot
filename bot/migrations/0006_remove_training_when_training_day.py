# Generated by Django 4.1.3 on 2024-03-14 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0005_alter_telegramuser_first_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="training",
            name="when",
        ),
        migrations.AddField(
            model_name="training",
            name="day",
            field=models.DateField(null=True),
        ),
    ]
