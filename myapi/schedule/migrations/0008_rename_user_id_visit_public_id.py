# Generated by Django 4.2.3 on 2023-07-07 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_remove_visit_revision_visit_revisions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visit',
            old_name='user_id',
            new_name='public_id',
        ),
    ]