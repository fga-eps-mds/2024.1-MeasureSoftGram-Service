# Generated by Django 4.0.6 on 2022-08-27 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
        ('metrics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectedmetric',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collected_metrics', to='organizations.repository'),
        ),
    ]
