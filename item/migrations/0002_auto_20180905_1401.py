# Generated by Django 2.1 on 2018-09-05 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemimage',
            name='image',
            field=models.ImageField(upload_to='.'),
        ),
    ]