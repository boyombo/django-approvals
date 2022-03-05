# Generated by Django 4.0.3 on 2022-03-05 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveIntegerField(choices=[(0, 'Pending'), (1, 'Approved'), (2, 'Rejected')], default=0)),
                ('object_model', models.CharField(max_length=100)),
                ('object_id', models.PositiveIntegerField()),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveIntegerField(choices=[], default=0)),
                ('step', models.PositiveIntegerField(default=1)),
                ('last_step', models.BooleanField(default=False)),
                ('approval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='approval.approval')),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_value', models.CharField(max_length=200)),
                ('final_value', models.CharField(max_length=200)),
                ('field_name', models.CharField(max_length=100)),
                ('approval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='approval.approval')),
            ],
        ),
    ]