# Generated by Django 2.0.2 on 2018-03-12 17:57

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('nombre', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=45)),
            ],
        ),
    ]
