# Generated by Django 5.0.6 on 2024-07-06 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercicios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigo',
            name='result',
            field=models.TextField(blank=True, null=True),
        ),
    ]
