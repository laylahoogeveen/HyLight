# Generated by Django 3.2.7 on 2022-03-20 16:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hl', '0012_question_colour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='colour',
            field=models.CharField(choices=[('orange', '(255,165,0)'), ('green', '(0,255,0)'), ('yellow', '(255,255,0)'), ('blue', '(0,0,255)'), ('purple', '(128,0,128)')], max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(blank=True, default=False)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_notification', to='hl.comment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]