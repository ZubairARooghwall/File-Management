# Generated by Django 4.2.2 on 2023-06-16 07:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0012_rename_prefers_dark_theme_user_prefer_dark_theme_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]