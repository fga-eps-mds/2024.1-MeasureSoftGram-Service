# Generated by Django 4.0.6 on 2024-09-04 23:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0011_merge_20231209_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReleaseConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('data', models.JSONField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='release_configuration', to='organizations.product')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
