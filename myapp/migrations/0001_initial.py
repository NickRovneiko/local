# Generated by Django 5.0.4 on 2024-04-20 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dialogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dialog_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('is_added', models.BooleanField(default=False)),
            ],
        ),
    ]