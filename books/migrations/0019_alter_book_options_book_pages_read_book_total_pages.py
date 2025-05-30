# Generated by Django 5.1.7 on 2025-05-20 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0018_profile_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={},
        ),
        migrations.AddField(
            model_name='book',
            name='pages_read',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='total_pages',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
