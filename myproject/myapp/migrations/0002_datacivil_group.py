# Generated by Django 4.2.3 on 2023-07-18 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datacivil',
            name='group',
            field=models.TextField(choices=[('A', 'Group A'), ('B', 'Group B'), ('C', 'Group C'), ('D', 'Group D')], default='', verbose_name='Grouping'),
        ),
    ]
