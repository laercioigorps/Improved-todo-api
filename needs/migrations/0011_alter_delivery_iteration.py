# Generated by Django 3.2.5 on 2021-08-22 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0010_auto_20210714_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='iteration',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='needs.iteration'),
        ),
    ]
