# Generated by Django 5.0.3 on 2024-04-01 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_class_in_subject_post_class_in_post_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='subject',
            new_name='name',
        ),
    ]