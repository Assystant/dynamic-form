import dynamic_form.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_form', '0008_backfill_variable_name_unique_prefix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='variable_name',
            field=models.CharField(editable=False, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='template',
            name='unique_prefix',
            field=models.CharField(default=dynamic_form.models.generate_unique_prefix, max_length=50, unique=True),
        ),
    ]
