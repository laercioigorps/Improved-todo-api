# Generated by Django 3.2.5 on 2021-10-07 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0016_need_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='need',
            name='icon',
        ),
        migrations.AddField(
            model_name='need',
            name='iconColor',
            field=models.CharField(default='', max_length=17),
        ),
        migrations.AddField(
            model_name='need',
            name='iconName',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.DeleteModel(
            name='Icon',
        ),
    ]