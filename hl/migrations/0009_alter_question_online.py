# Generated by Django 3.2.7 on 2022-03-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hl', '0008_auto_20220316_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='online',
            field=models.BooleanField(blank=True, choices=[(True, 'Online'), (False, 'On campus')], default=False),
        ),
    ]