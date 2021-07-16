# Generated by Django 3.2.5 on 2021-07-16 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrower',
            name='is_borrower',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='investor',
            name='is_investor',
            field=models.BooleanField(default=True),
        ),
    ]