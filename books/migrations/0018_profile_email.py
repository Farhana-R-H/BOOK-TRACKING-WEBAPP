# Generated by Django 5.1.7 on 2025-05-20 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0017_remove_profile_email_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
