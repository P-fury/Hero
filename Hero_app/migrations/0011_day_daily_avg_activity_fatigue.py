# Generated by Django 5.0.4 on 2024-04-07 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hero_app', '0010_alter_day_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='daily_avg_activity_fatigue',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
