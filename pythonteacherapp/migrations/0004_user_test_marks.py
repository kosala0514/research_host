# Generated by Django 4.1.1 on 2023-03-17 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pythonteacherapp', '0003_auto_20230317_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='test_marks',
            field=models.FloatField(default='0.00', editable=False, max_length=15),
        ),
    ]