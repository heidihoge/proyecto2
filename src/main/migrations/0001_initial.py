# Generated by Django 2.0.2 on 2018-04-06 00:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
                ('monto', models.IntegerField()),
                ('saldo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=8, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('fecha_nacimiento', models.DateField(default=datetime.date.today)),
                ('sexo', models.CharField(choices=[('F', 'FEMENINO'), ('M', 'MASCULINO')], max_length=1)),
                ('direccion', models.CharField(max_length=50)),
                ('telefono1', models.CharField(blank=True, max_length=50, null=True)),
                ('telefono2', models.CharField(blank=True, max_length=50, null=True)),
                ('fotocopia_cedula', models.ImageField(blank=True, null=True, upload_to='media_root', verbose_name='Fotocopia de Cédula')),
                ('estado', models.CharField(choices=[('A', 'ACTIVO'), ('IN', 'INACTIVO')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Persona')),
                ('imagen', models.ImageField(upload_to='media_root', verbose_name='Foto')),
                ('ficha', models.FileField(upload_to='media_root', verbose_name='Ficha médica')),
                ('ficha_inscripcion', models.FileField(upload_to='media_root', verbose_name='Ficha de inscripción')),
            ],
            bases=('main.persona',),
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Persona')),
                ('salario', models.IntegerField(default=0)),
            ],
            bases=('main.persona',),
        ),
        migrations.CreateModel(
            name='Titular',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Persona')),
                ('tipo_responsable', models.CharField(choices=[('M', 'Madre'), ('P', 'Padre'), ('H', 'Hermano/a'), ('T', 'Tio/a'), ('A', 'Abuelo/a'), ('E', 'Encargado/a'), ('U', 'Unico')], max_length=1)),
            ],
            bases=('main.persona',),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='id_persona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Persona'),
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('empleado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Empleado')),
                ('especialidad', models.CharField(max_length=50)),
            ],
            bases=('main.empleado',),
        ),
        migrations.AddField(
            model_name='alumno',
            name='titular_cuenta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Titular'),
        ),
    ]
