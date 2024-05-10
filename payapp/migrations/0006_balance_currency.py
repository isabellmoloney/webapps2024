# Generated by Django 4.2.11 on 2024-05-09 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0005_conversionresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='currency',
            field=models.CharField(choices=[('GBP', 'British pounds'), ('EUR', 'Euro'), ('USD', 'US Dollar')], default='GBP', max_length=3),
        ),
    ]