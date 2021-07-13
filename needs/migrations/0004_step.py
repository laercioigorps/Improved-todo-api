# Generated by Django 3.2.5 on 2021-07-13 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0003_goal_enddate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(default='', max_length=80)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]
