# Generated by Django 5.0.4 on 2024-04-22 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='user_id',
            field=models.BigIntegerField(null=True),
        ),
    ]