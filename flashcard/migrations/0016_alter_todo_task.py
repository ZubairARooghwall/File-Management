# Generated by Django 4.2.2 on 2023-06-16 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0015_alter_notes_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='task',
            field=models.TextField(max_length=300),
        ),
    ]