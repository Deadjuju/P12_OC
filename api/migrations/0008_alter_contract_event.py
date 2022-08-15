# Generated by Django 4.1 on 2022-08-15 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_contract_event_alter_contract_payment_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events_contract', to='api.event'),
        ),
    ]