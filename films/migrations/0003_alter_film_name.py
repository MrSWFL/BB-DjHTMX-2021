# Generated by Django 3.2.8 on 2024-05-28 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_film'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
