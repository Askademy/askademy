# Generated by Django 4.2.5 on 2023-11-05 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='code',
            field=models.CharField(default='769364', editable=False, max_length=100),
        ),
    ]