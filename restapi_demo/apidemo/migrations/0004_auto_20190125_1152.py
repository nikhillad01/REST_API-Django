# Generated by Django 2.1.5 on 2019-01-25 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apidemo', '0003_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='email',
            field=models.CharField(max_length=30),
        ),
    ]
