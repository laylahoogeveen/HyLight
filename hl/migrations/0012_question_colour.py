# Generated by Django 3.2.7 on 2022-03-17 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hl', '0011_alter_comment_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='colour',
            field=models.CharField(choices=[('white', '(255,255,255)'), ('orange', '(255,165,0)'), ('green', '(0,255,0)'), ('yellow', '(255,255,0)'), ('blue', '(0,0,255)'), ('purple', '(128,0,128)')], default='white', max_length=20, null=True),
        ),
    ]
