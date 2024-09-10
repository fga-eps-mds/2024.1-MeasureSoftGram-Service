# Generated by Django 4.0.6 on 2022-08-25 20:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('metrics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportedMeasure',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('key', models.CharField(max_length=128, unique=True)),
                ('name', models.CharField(max_length=128)),
                (
                    'description',
                    models.TextField(blank=True, max_length=512, null=True),
                ),
                (
                    'metrics',
                    models.ManyToManyField(
                        blank=True,
                        related_name='related_measures',
                        to='metrics.supportedmetric',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='CalculatedMeasure',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('value', models.FloatField()),
                (
                    'created_at',
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    'measure',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='calculated_measures',
                        to='measures.supportedmeasure',
                    ),
                ),
                (
                    'repository',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='calculated_measures',
                        to='organizations.repository',
                    ),
                ),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
