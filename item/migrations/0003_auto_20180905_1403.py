# Generated by Django 2.1 on 2018-09-05 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_auto_20180905_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemimage',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]