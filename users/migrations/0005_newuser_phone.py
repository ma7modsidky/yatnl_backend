# Generated by Django 4.0.6 on 2022-07-07 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_newuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
