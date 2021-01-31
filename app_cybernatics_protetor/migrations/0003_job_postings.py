# Generated by Django 2.1.4 on 2019-02-03 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cybernatics_protetor', '0002_success_stories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job_Postings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Job', models.CharField(max_length=30)),
                ('Title', models.CharField(max_length=30)),
                ('Qualification', models.CharField(max_length=50)),
                ('Percentage', models.IntegerField()),
                ('Experience', models.IntegerField(help_text='In Years')),
                ('Last_date', models.DateField()),
                ('Location', models.CharField(max_length=100)),
                ('Salary', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
