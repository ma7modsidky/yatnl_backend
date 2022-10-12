# Generated by Django 4.0.6 on 2022-07-20 17:33

from django.db import migrations, models
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_leader_id_alter_leader_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='leader',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='leader',
            name='uuid',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, db_index=True, editable=False, max_length=22),
        ),
    ]