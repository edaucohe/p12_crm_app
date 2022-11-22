# Generated by Django 4.1.1 on 2022-11-21 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0002_alter_contract_amount'),
        ('events', '0002_event_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='contract',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='contracts.contract'),
            preserve_default=False,
        ),
    ]
