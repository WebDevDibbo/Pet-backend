# Generated by Django 5.0.6 on 2024-11-14 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adoption', '0001_initial'),
        ('users', '0002_rename_users_userprofilemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoption',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adoptions', to='users.userprofilemodel'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofilemodel'),
        ),
    ]
