# Generated by Django 3.2.13 on 2024-06-12 22:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dosage', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicines', to='core.patient')),
            ],
        ),
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateField()),
                ('description', models.TextField()),
                ('blood_pressure', models.CharField(blank=True, max_length=10, null=True)),
                ('heart_rate', models.IntegerField(blank=True, null=True)),
                ('temperature', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('blood_group', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3, null=True)),
                ('diseases', models.CharField(choices=[('None', 'None'), ('HIV', 'HIV'), ('COVID', 'COVID'), ('Diabetes', 'Diabetes'), ('Hypertension', 'Hypertension'), ('Cancer', 'Cancer')], default='None', max_length=20)),
                ('surgery_history', models.CharField(choices=[('None', 'None'), ('Appendectomy', 'Appendectomy'), ('Cardiac Surgery', 'Cardiac Surgery'), ('Orthopedic Surgery', 'Orthopedic Surgery'), ('Neurosurgery', 'Neurosurgery')], default='None', max_length=50)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_records', to='core.patient')),
            ],
        ),
    ]
