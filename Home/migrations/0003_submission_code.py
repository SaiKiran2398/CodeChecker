# Generated by Django 4.0.3 on 2022-04-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_remove_problem_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='code',
            field=models.TextField(null=True),
        ),
    ]
