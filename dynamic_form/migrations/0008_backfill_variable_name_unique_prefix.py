"""Fill in Template.unique_prefix and Field.variable_name before 0009 makes them unique.

0007 added both columns as nullable so existing rows could take them. Rows saved
before 0007 (or through code paths that skipped save()) can hold NULL or '' there,
and nothing in the database stopped duplicates. This migration gives every such row
a value, using the same rules as the model code, and leaves rows that already hold a
value of their own alone (only the second and later copies of a duplicate change).

It is separate from 0009 on purpose: on PostgreSQL, updating rows and then adding a
unique constraint to the same table inside one transaction can fail with "pending
trigger events".
"""
import re
import uuid

from django.db import migrations


def _new_prefix(used):
    while True:
        prefix = f"form_{uuid.uuid4().hex[:8]}"
        if prefix not in used:
            return prefix


def _variable_name(field, prefix, used):
    base_name = re.sub(r'\W+', '_', (field.label or '').strip().lower())
    variable_name = f"{prefix}_{base_name}_{field.type}"
    unique_name = variable_name
    count = 1
    while unique_name in used:
        unique_name = f"{variable_name}_{count}"
        count += 1
    return unique_name


def backfill(apps, schema_editor):
    Template = apps.get_model('dynamic_form', 'Template')
    Field = apps.get_model('dynamic_form', 'Field')

    # Templates first: a field's variable name is built from its template's prefix.
    used_prefixes = set()
    for template in Template.objects.order_by('id').only('id', 'unique_prefix'):
        prefix = template.unique_prefix
        if not prefix or prefix in used_prefixes:
            prefix = _new_prefix(used_prefixes)
            Template.objects.filter(pk=template.pk).update(unique_prefix=prefix)
        used_prefixes.add(prefix)

    prefixes = dict(Template.objects.values_list('id', 'unique_prefix'))
    used_names = set()
    for field in Field.objects.order_by('id').only('id', 'label', 'type', 'template_id', 'variable_name'):
        name = field.variable_name
        if not name or name in used_names:
            name = _variable_name(field, prefixes[field.template_id], used_names)
            Field.objects.filter(pk=field.pk).update(variable_name=name)
        used_names.add(name)


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_form', '0007_field_variable_name_template_unique_prefix_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill, migrations.RunPython.noop),
    ]
