# Generated by Django 3.2.13 on 2024-06-18 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_alter_healthrecord_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_date', models.DateField()),
                ('exercise_type', models.CharField(choices=[('Cardio', 'Cardio'), ('Strength Training', 'Strength Training'), ('Flexibility', 'Flexibility'), ('Balance', 'Balance')], max_length=20)),
                ('duration_minutes', models.PositiveIntegerField()),
                ('calories_burned', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_tracker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
