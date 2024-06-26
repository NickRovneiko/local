# Generated by Django 5.0.4 on 2024-04-22 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_delete_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.BigIntegerField(unique=True)),
                ('user_id', models.BigIntegerField()),
                ('date', models.DateTimeField()),
                ('text', models.TextField()),
                ('dialogue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='myapp.dialogue')),
            ],
        ),
    ]
