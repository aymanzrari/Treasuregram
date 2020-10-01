# Generated by Django 2.1.5 on 2019-02-26 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0003_auto_20190226_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treasure',
            name='img_url',
        ),
        migrations.AddField(
            model_name='treasure',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
