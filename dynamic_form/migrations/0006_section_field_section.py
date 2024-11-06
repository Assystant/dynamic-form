# Generated by Django 5.0.6 on 2024-07-04 08:01

import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_form', '0005_field_allow_specific_file_type_field_file_types_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('label', models.CharField(blank=True, default='', max_length=5000)),
                ('description', models.TextField(blank=True, default='')),
                ('sort_order', models.PositiveBigIntegerField(blank=True, default=0)),
                ('template', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='dynamic_form.template')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='field',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fields', to='dynamic_form.section'),
        ),
    ]