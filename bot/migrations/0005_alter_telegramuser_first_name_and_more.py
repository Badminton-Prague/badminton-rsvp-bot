# Generated by Django 4.1.3 on 2024-03-05 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0004_training_when"),
    ]

    operations = [
        migrations.AlterField(
            model_name="telegramuser",
            name="first_name",
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name="telegramuser",
            name="last_name",
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name="telegramuser",
            name="username",
            field=models.CharField(max_length=512, null=True),
        ),
    ]