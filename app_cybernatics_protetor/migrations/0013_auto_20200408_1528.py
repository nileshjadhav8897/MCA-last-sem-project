# Generated by Django 2.2.3 on 2020-04-08 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cybernatics_protetor', '0012_casecreation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createagent',
            name='Agent_Name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
