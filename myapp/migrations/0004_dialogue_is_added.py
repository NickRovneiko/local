# Generated by Django 5.0.4 on 2024-04-20 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_dialog_id_dialogue_dialogue_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialogue',
            name='is_added',
            field=models.BooleanField(default=False),
        ),
    ]
