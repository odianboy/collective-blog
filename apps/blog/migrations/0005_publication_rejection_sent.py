# Generated by Django 3.1.7 on 2021-02-26 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_publication_rejection_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='rejection_sent',
            field=models.BooleanField(default=False),
        ),
    ]
