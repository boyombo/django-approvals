# Generated by Django 4.0.3 on 2022-03-05 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0002_rename_object_model_approval_model_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvalchange',
            name='field_type',
            field=models.PositiveIntegerField(choices=[(0, 'Char'), (1, 'Int'), (2, 'Float'), (3, 'FK')], default=0),
        ),
    ]